import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client, Client

# Add parent directory to sys.path so app modules can be imported if needed
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


def validate_environment() -> dict:
    """Validate and return required environment variables from .env."""
    env_path = Path(__file__).resolve().parent.parent / ".env"
    load_dotenv(dotenv_path=env_path)

    required_vars = [
        "SUPABASE_URL",
        "SUPABASE_SERVICE_ROLE_KEY",
        "DEMO_DOCTOR_PASSWORD",
        "DEMO_PATIENT_PASSWORD",
    ]

    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        print(f"[FATAL] Missing required environment variable(s): {', '.join(missing)}")
        print(f"Please check your .env file at: {env_path}")
        sys.exit(1)

    return {
        "supabase_url": os.getenv("SUPABASE_URL"),
        "supabase_service_role_key": os.getenv("SUPABASE_SERVICE_ROLE_KEY"),
        "demo_doctor_password": os.getenv("DEMO_DOCTOR_PASSWORD"),
        "demo_patient_password": os.getenv("DEMO_PATIENT_PASSWORD"),
    }


def fetch_all_auth_users(client: Client) -> dict[str, str]:
    """
    Fetch all existing Supabase Auth users using pagination.
    Returns a dictionary mapping lowercased email -> user UUID.
    """
    email_to_id = {}
    page = 1
    per_page = 50

    while True:
        try:
            res = client.auth.admin.list_users(page=page, per_page=per_page)
            # res can be a list or an object with .users depending on supabase-py / gotrue version
            users = res if isinstance(res, list) else getattr(res, "users", [])
            if not users:
                break

            for u in users:
                email = getattr(u, "email", None) or (u.get("email") if isinstance(u, dict) else None)
                uid = getattr(u, "id", None) or (u.get("id") if isinstance(u, dict) else None)
                if email and uid:
                    email_to_id[email.strip().lower()] = str(uid)

            if len(users) < per_page:
                break
            page += 1
        except Exception as e:
            print(f"[ERROR] Failed to fetch auth users on page {page}: {e}")
            raise

    return email_to_id


def get_or_create_auth_user(
    client: Client,
    email: str,
    password: str,
    full_name: str,
    existing_auth_users: dict[str, str],
) -> tuple[str, str]:
    """
    Idempotently find or create an auth user.
    Returns (auth_user_id, status) where status is 'EXISTING' or 'CREATED'.
    """
    normalized_email = email.strip().lower()

    # If already in Auth
    if normalized_email in existing_auth_users:
        return existing_auth_users[normalized_email], "EXISTING"

    # Create new Supabase Auth user
    try:
        user_attributes = {
            "email": normalized_email,
            "password": password,
            "email_confirm": True,
            "user_metadata": {"full_name": full_name},
        }
        res = client.auth.admin.create_user(user_attributes)
        user = getattr(res, "user", res)
        uid = str(getattr(user, "id", None) or (user.get("id") if isinstance(user, dict) else None))
        existing_auth_users[normalized_email] = uid
        return uid, "CREATED"
    except Exception as e:
        error_msg = str(e).lower()
        if "already registered" in error_msg or "already exists" in error_msg:
            # Fallback: re-fetch auth users if there was a race condition
            refetched = fetch_all_auth_users(client)
            existing_auth_users.update(refetched)
            if normalized_email in existing_auth_users:
                return existing_auth_users[normalized_email], "EXISTING"
        raise RuntimeError(f"Failed to create Auth user for {email}: {e}") from e


def link_users():
    """Main execution function for bootstrapping Auth accounts and linking them to seeded DB records."""
    config = validate_environment()

    print("\nConnecting to Supabase using service-role key...")
    try:
        supabase: Client = create_client(
            config["supabase_url"],
            config["supabase_service_role_key"]
        )
    except Exception as e:
        print(f"[FATAL] Failed to initialize Supabase client: {e}")
        sys.exit(1)

    # 1. Read seeded doctors from public.doctors
    print("Fetching seeded doctors from public.doctors...")
    try:
        doctors_res = supabase.table("doctors").select("doctor_id, full_name, email, auth_user_id").execute()
        doctors = doctors_res.data or []
    except Exception as e:
        print("\n" + "=" * 80)
        print("[FATAL ERROR] Unable to read 'public.doctors' from Supabase.")
        print(f"Details: {e}")
        print("\nThis usually occurs when the service_role lacks table permissions.")
        print("Please execute the following SQL in Supabase Dashboard -> SQL Editor:")
        print("-" * 80)
        print("GRANT ALL ON ALL TABLES IN SCHEMA public TO service_role;")
        print("GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO service_role;")
        print("GRANT ALL ON ALL ROUTINES IN SCHEMA public TO service_role;")
        print("-" * 80)
        print("=" * 80 + "\n")
        sys.exit(1)

    # 2. Read seeded patients from public.patients
    print("Fetching seeded patients from public.patients...")
    try:
        patients_res = supabase.table("patients").select("patient_id, full_name, email, auth_user_id").execute()
        patients = patients_res.data or []
    except Exception as e:
        print("\n" + "=" * 80)
        print("[FATAL ERROR] Unable to read 'public.patients' from Supabase.")
        print(f"Details: {e}")
        print("=" * 80 + "\n")
        sys.exit(1)

    if not doctors:
        print("[ERROR] No seeded rows found in 'public.doctors'. Aborting.")
        sys.exit(1)
    if not patients:
        print("[ERROR] No seeded rows found in 'public.patients'. Aborting.")
        sys.exit(1)

    print(f"Found {len(doctors)} seeded doctor(s) and {len(patients)} seeded patient(s).")

    # 3. Retrieve existing Supabase Auth users
    print("Retrieving existing Supabase Auth users...")
    auth_users_cache = fetch_all_auth_users(client=supabase)
    print(f"Existing Auth users in Supabase: {len(auth_users_cache)}")

    summary_rows = []
    created_count = 0
    existing_count = 0
    linked_count = 0
    failed_count = 0

    # 4. Bootstrap Doctors
    for doc in doctors:
        doc_id = doc["doctor_id"]
        full_name = doc.get("full_name") or "Doctor"
        email = doc.get("email")

        if not email:
            print(f"[WARN] Doctor {doc_id} ({full_name}) has no email. Skipping.")
            failed_count += 1
            continue

        try:
            auth_uid, status = get_or_create_auth_user(
                client=supabase,
                email=email,
                password=config["demo_doctor_password"],
                full_name=full_name,
                existing_auth_users=auth_users_cache,
            )
            if status == "CREATED":
                created_count += 1
            else:
                existing_count += 1

            # Upsert user_roles (auth_user_id, role)
            supabase.table("user_roles").upsert(
                {"auth_user_id": auth_uid, "role": "DOCTOR"},
                on_conflict="auth_user_id"
            ).execute()

            # Update doctors.auth_user_id if not already set or changed
            if doc.get("auth_user_id") != auth_uid:
                supabase.table("doctors").update({"auth_user_id": auth_uid}).eq("doctor_id", doc_id).execute()

            linked_count += 1
            summary_rows.append((full_name, "DOCTOR", email, auth_uid, status))

        except Exception as e:
            print(f"[ERROR] Failed processing doctor {full_name} ({email}): {e}")
            summary_rows.append((full_name, "DOCTOR", email, "FAILED", f"ERROR: {e}"))
            failed_count += 1

    # 5. Bootstrap Patients
    for pat in patients:
        pat_id = pat["patient_id"]
        full_name = pat.get("full_name") or "Patient"
        email = pat.get("email")

        if not email:
            print(f"[WARN] Patient {pat_id} ({full_name}) has no email. Skipping.")
            failed_count += 1
            continue

        try:
            auth_uid, status = get_or_create_auth_user(
                client=supabase,
                email=email,
                password=config["demo_patient_password"],
                full_name=full_name,
                existing_auth_users=auth_users_cache,
            )
            if status == "CREATED":
                created_count += 1
            else:
                existing_count += 1

            # Upsert user_roles (auth_user_id, role)
            supabase.table("user_roles").upsert(
                {"auth_user_id": auth_uid, "role": "PATIENT"},
                on_conflict="auth_user_id"
            ).execute()

            # Update patients.auth_user_id if not already set or changed
            if pat.get("auth_user_id") != auth_uid:
                supabase.table("patients").update({"auth_user_id": auth_uid}).eq("patient_id", pat_id).execute()

            linked_count += 1
            summary_rows.append((full_name, "PATIENT", email, auth_uid, status))

        except Exception as e:
            print(f"[ERROR] Failed processing patient {full_name} ({email}): {e}")
            summary_rows.append((full_name, "PATIENT", email, "FAILED", f"ERROR: {e}"))
            failed_count += 1

    # 6. Print Formatted Summary
    print("\nMediTrace Auth Bootstrap")
    print("========================")
    print(f"\n{'Name':<24} {'Role':<10} {'Email':<30} {'Auth UUID':<38} {'Status':<10}")
    print("-" * 116)
    for name, role, email, uid, status in summary_rows:
        print(f"{name:<24} {role:<10} {email:<30} {uid:<38} {status:<10}")

    total_candidates = len(doctors) + len(patients)
    print("\n" + "-" * 116)
    print(f"Total: {total_candidates}")
    print(f"Created: {created_count}")
    print(f"Existing: {existing_count}")
    print(f"Linked: {linked_count}")
    print(f"Failed: {failed_count}")
    print("=" * 116 + "\n")

    if failed_count > 0:
        sys.exit(1)


if __name__ == "__main__":
    link_users()
