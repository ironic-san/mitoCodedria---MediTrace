from abc import ABC, abstractmethod
from datetime import datetime, timezone
import hashlib
import logging
import os
import uuid
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class BlockchainAdapter(ABC):
    """Abstract Base Class for Hyperledger Fabric blockchain adapters."""

    @abstractmethod
    def anchor_record(self, event_id: str, canonical_hash: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Anchors a canonical record hash to the blockchain ledger."""
        pass

    def anchor_event(
        self,
        event_id: str,
        patient_id: str,
        event_hash: str,
        event_title: str = "Critical Medical Event",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Convenience method to anchor an event with named parameters."""
        meta = metadata.copy() if metadata else {}
        meta["patient_id"] = patient_id
        meta["title"] = event_title
        proof = self.anchor_record(event_id=event_id, canonical_hash=event_hash, metadata=meta)
        proof.setdefault("blockchain_network", "Hyperledger Fabric (meditrace-channel)")
        return proof

    @abstractmethod
    def verify_proof(self, event_id: str, canonical_hash: str) -> Dict[str, Any]:
        """Verifies whether a canonical hash matches the anchored ledger state."""
        pass

    @abstractmethod
    def get_proof(self, event_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves historical blockchain proof for an event."""
        pass

    @abstractmethod
    def get_channel_info(self) -> Dict[str, Any]:
        """Returns metadata about the Fabric channel and chaincode."""
        pass


class MockFabricAdapter(BlockchainAdapter):
    """
    Deterministic development and hackathon demo adapter simulating Hyperledger Fabric.
    Maintains an immutable ledger state representing channel 'meditrace-channel'
    and chaincode 'medical_integrity_cc'.
    """

    def __init__(self):
        self.channel_name = "meditrace-channel"
        self.chaincode_name = "medical_integrity_cc"
        self.msp_id = "Org1MSP"
        self._current_block_number = 100020
        # In-memory immutable blockchain state: event_id -> proof dict
        self._ledger: Dict[str, Dict[str, Any]] = {}
        self._seed_initial_demo_ledger()

    def _seed_initial_demo_ledger(self):
        """Pre-seeds the ledger with the demo patient historical proofs."""
        initial_proofs = [
            {
                "event_id": "70000000-0000-0000-0000-000000000001",
                "patient_id": "20000000-0000-0000-0000-000000000001",
                "event_hash": "52046f623c8ef75884c2d4119f61bbc3d4036f7ba6be21e92baa3ebe8456d4f2",
                "blockchain_tx_id": "demo-tx-aarav-fracture",
                "block_number": 100001,
                "blockchain_timestamp": "2026-09-14T03:30:00+00:00",
                "title": "Left Femur Fracture",
            },
            {
                "event_id": "70000000-0000-0000-0000-000000000002",
                "patient_id": "20000000-0000-0000-0000-000000000001",
                "event_hash": "55e21c4d766cfac8d333e90b122e3c00f65c3addaea16f1e73f840731a714d61",
                "blockchain_tx_id": "demo-tx-aarav-surgery",
                "block_number": 100002,
                "blockchain_timestamp": "2026-09-14T03:30:00+00:00",
                "title": "Intramedullary Femur Fixation",
            },
            {
                "event_id": "70000000-0000-0000-0000-000000000005",
                "patient_id": "20000000-0000-0000-0000-000000000003",
                "event_hash": "c1b8f1827d2bfc3f22831fc40a948c7308ae569487b096d94b74007c57e95a2f",
                "blockchain_tx_id": "demo-tx-nikhil-mi",
                "block_number": 100003,
                "blockchain_timestamp": "2026-09-14T03:30:00+00:00",
                "title": "Acute Myocardial Infarction",
            },
            {
                "event_id": "70000000-0000-0000-0000-000000000006",
                "patient_id": "20000000-0000-0000-0000-000000000003",
                "event_hash": "b92ce66b8a757092c3bb1ac68fc54e78f0b87eca0a6ab018eb4443488cda552c",
                "blockchain_tx_id": "demo-tx-nikhil-stent",
                "block_number": 100004,
                "blockchain_timestamp": "2026-09-14T03:30:00+00:00",
                "title": "Coronary Angioplasty and Stent",
            },
            {
                "event_id": "70000000-0000-0000-0000-000000000007",
                "patient_id": "20000000-0000-0000-0000-000000000004",
                "event_hash": "5637c2d893e5e163f03bc452a37607eaec7b617810f6cacf29316276b5f89ca2",
                "blockchain_tx_id": "demo-tx-diya-cancer",
                "block_number": 100005,
                "blockchain_timestamp": "2026-09-14T03:30:00+00:00",
                "title": "Osteosarcoma Diagnosed",
            },
            {
                "event_id": "70000000-0000-0000-0000-000000000008",
                "patient_id": "20000000-0000-0000-0000-000000000004",
                "event_hash": "bad81d8018e78c0da53d56eb7e20e371dc3b55d9e2281471e01a3718bfdec6ca",
                "blockchain_tx_id": "demo-tx-diya-chemo",
                "block_number": 100006,
                "blockchain_timestamp": "2026-09-14T03:30:00+00:00",
                "title": "Chemotherapy Started",
            },
            {
                "event_id": "70000000-0000-0000-0000-000000000010",
                "patient_id": "20000000-0000-0000-0000-000000000005",
                "event_hash": "39bfe0d55bf85554c6cb4164c243ced01b732cd7ffb31df7fab9bd4a5192fd68",
                "blockchain_tx_id": "demo-tx-kabir-penicillin",
                "block_number": 100007,
                "blockchain_timestamp": "2026-09-14T03:30:00+00:00",
                "title": "Penicillin Allergy Confirmed",
            },
            {
                "event_id": "70000000-0000-0000-0000-000000000012",
                "patient_id": "20000000-0000-0000-0000-000000000006",
                "event_hash": "8eff533b488c9e58715760afbdd774020a97e9f8d148d0b91815180ba1838b60",
                "blockchain_tx_id": "demo-tx-tanya-brain-surgery",
                "block_number": 100008,
                "blockchain_timestamp": "2026-09-14T03:30:00+00:00",
                "title": "Brain Surgery",
            },
        ]
        for p in initial_proofs:
            self._ledger[p["event_id"]] = p

    def anchor_record(self, event_id: str, canonical_hash: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        self._current_block_number += 1
        tx_id = f"fabric-tx-{uuid.uuid4().hex[:16]}"
        now_iso = datetime.now(timezone.utc).isoformat()

        proof = {
            "event_id": event_id,
            "patient_id": metadata.get("patient_id"),
            "event_hash": canonical_hash,
            "blockchain_tx_id": tx_id,
            "block_number": self._current_block_number,
            "blockchain_timestamp": now_iso,
            "channel": self.channel_name,
            "chaincode": self.chaincode_name,
            "blockchain_network": "Hyperledger Fabric (meditrace-channel)",
            "endorsed_by": [self.msp_id],
            "title": metadata.get("title", "Medical Event"),
        }
        self._ledger[event_id] = proof
        logger.info(f"[Fabric Mock] Anchored event {event_id} at block {self._current_block_number} with tx {tx_id}")
        return proof

    def verify_proof(self, event_id: str, canonical_hash: str) -> Dict[str, Any]:
        proof = self._ledger.get(event_id)
        if not proof:
            return {
                "anchored": False,
                "verified": False,
                "status": "NOT_ANCHORED",
                "message": f"No blockchain proof found for event ID '{event_id}'.",
                "proof": None,
            }

        anchored_hash = proof.get("event_hash")
        if anchored_hash == canonical_hash:
            return {
                "anchored": True,
                "verified": True,
                "status": "VERIFIED",
                "message": "Cryptographic integrity verified. Current record matches the immutable blockchain ledger.",
                "proof": proof,
            }
        else:
            return {
                "anchored": True,
                "verified": False,
                "status": "TAMPERED_OR_MODIFIED",
                "message": "Integrity check failed. Current record hash does not match anchored blockchain hash.",
                "proof": proof,
            }

    def get_proof(self, event_id: str) -> Optional[Dict[str, Any]]:
        return self._ledger.get(event_id)

    def get_channel_info(self) -> Dict[str, Any]:
        return {
            "adapter": "MockFabricAdapter (Development/Hackathon Demo)",
            "channel": self.channel_name,
            "chaincode": self.chaincode_name,
            "msp_id": self.msp_id,
            "current_block": self._current_block_number,
            "total_anchored_proofs": len(self._ledger),
        }


class HyperledgerFabricGatewayAdapter(BlockchainAdapter):
    """
    Production Hyperledger Fabric Gateway client adapter.
    Connects to live Fabric peers via gRPC / Fabric Gateway SDK.
    """

    def __init__(self):
        self.peer_endpoint = os.getenv("FABRIC_PEER_ENDPOINT", "localhost:7051")
        self.channel_name = os.getenv("FABRIC_CHANNEL_NAME", "meditrace-channel")
        self.chaincode_name = os.getenv("FABRIC_CHAINCODE_NAME", "medical_integrity_cc")
        self.msp_id = os.getenv("FABRIC_MSP_ID", "Org1MSP")
        self.cert_path = os.getenv("FABRIC_CERT_PATH", "")
        self.key_path = os.getenv("FABRIC_KEY_PATH", "")

    def anchor_record(self, event_id: str, canonical_hash: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError("Live Hyperledger Fabric Gateway requires operational Fabric network endpoint.")

    def verify_proof(self, event_id: str, canonical_hash: str) -> Dict[str, Any]:
        raise NotImplementedError("Live Hyperledger Fabric Gateway requires operational Fabric network endpoint.")

    def get_proof(self, event_id: str) -> Optional[Dict[str, Any]]:
        raise NotImplementedError("Live Hyperledger Fabric Gateway requires operational Fabric network endpoint.")

    def get_channel_info(self) -> Dict[str, Any]:
        return {
            "adapter": "HyperledgerFabricGatewayAdapter (Live Gateway)",
            "peer_endpoint": self.peer_endpoint,
            "channel": self.channel_name,
            "chaincode": self.chaincode_name,
            "msp_id": self.msp_id,
        }


# Singleton adapter instance
_adapter_instance: Optional[BlockchainAdapter] = None


def get_blockchain_service() -> BlockchainAdapter:
    """
    Returns the active blockchain adapter.
    Uses HyperledgerFabricGatewayAdapter if FABRIC_ENABLED is set to true,
    otherwise uses the MockFabricAdapter for development and testing.
    """
    global _adapter_instance
    if _adapter_instance is None:
        fabric_enabled = os.getenv("FABRIC_ENABLED", "false").lower() in {"true", "1", "yes"}
        if fabric_enabled and os.getenv("FABRIC_PEER_ENDPOINT"):
            _adapter_instance = HyperledgerFabricGatewayAdapter()
        else:
            _adapter_instance = MockFabricAdapter()
    return _adapter_instance
