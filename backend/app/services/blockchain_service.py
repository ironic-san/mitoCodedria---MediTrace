from abc import ABC, abstractmethod
import os
from typing import Any, Dict, Optional

import httpx


class BlockchainAdapter(ABC):
    @abstractmethod
    def anchor_event(
        self,
        proof_id: str,
        subject_ref: str,
        event_hash: str,
        record_version: int,
        previous_proof_hash: Optional[str] = None,
        status: str = "ACTIVE",
    ) -> Dict[str, Any]:
        pass

    @abstractmethod
    def verify_proof(self, proof_id: str, event_hash: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_proof(self, proof_id: str) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_patient_proofs(self, subject_ref: str) -> list:
        pass

    @abstractmethod
    def get_channel_info(self) -> Dict[str, Any]:
        pass


class HyperledgerFabricGatewayAdapter(BlockchainAdapter):
    """HTTP client for the real MediTrace Blockchain Service."""

    def __init__(self):
        self.base_url = os.getenv(
            "BLOCKCHAIN_SERVICE_URL",
            "http://localhost:3001",
        ).rstrip("/")
        self.timeout = float(
            os.getenv("BLOCKCHAIN_SERVICE_TIMEOUT", "10")
        )

    def _get(self, path: str):
        response = httpx.get(
            f"{self.base_url}{path}",
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    def _post(self, path: str, payload: Dict[str, Any]):
        response = httpx.post(
            f"{self.base_url}{path}",
            json=payload,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    def anchor_event(
        self,
        proof_id: str,
        subject_ref: str,
        event_hash: str,
        record_version: int,
        previous_proof_hash: Optional[str] = None,
        status: str = "ACTIVE",
    ) -> Dict[str, Any]:
        return self._post(
            "/integrity/register",
            {
                "proofId": proof_id,
                "subjectRef": subject_ref,
                "eventHash": event_hash,
                "recordVersion": int(record_version),
                "previousProofHash": previous_proof_hash or "",
                "status": status,
            },
        )

    def verify_proof(
        self,
        proof_id: str,
        event_hash: str,
    ) -> Dict[str, Any]:
        return self._post(
            "/integrity/verify",
            {
                "proofId": proof_id,
                "eventHash": event_hash,
            },
        )

    def get_proof(self, proof_id: str) -> Optional[Dict[str, Any]]:
        try:
            return self._get(
                f"/integrity/proofs/{proof_id}"
            )
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 404:
                return None
            raise

    def get_patient_proofs(self, subject_ref: str) -> list:
        return self._get(
            f"/integrity/patient/{subject_ref}"
        )

    def get_channel_info(self) -> Dict[str, Any]:
        return {
            "adapter": "HyperledgerFabricGatewayAdapter",
            "service_url": self.base_url,
            "channel": "mychannel",
            "chaincode": "meditrace",
            "msp_id": "Org1MSP",
        }


_adapter_instance: Optional[BlockchainAdapter] = None


def get_blockchain_service() -> BlockchainAdapter:
    global _adapter_instance

    if _adapter_instance is None:
        _adapter_instance = HyperledgerFabricGatewayAdapter()

    return _adapter_instance
