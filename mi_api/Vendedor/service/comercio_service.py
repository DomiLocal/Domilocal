# ─────────────────────────────────────
# SERVICE LAYER
# Business logic
# ─────────────────────────────────────

from domain.comercio import (
    MerchantCreate,
    MerchantResponse,
    MerchantRegistrationResponse
)

from repository.comercio_repository import (
    MerchantRepository
)


class MerchantService:


    def __init__(
        self,
        repo: MerchantRepository
    ):

        self.repo=repo


    def register(
        self,
        data: MerchantCreate
    ):


        existing_merchant = self.repo.get_by_name_address(

            data.name,
            data.address

        )


        if existing_merchant:

            raise ValueError(
                "A merchant with that name and address already exists."
            )


        new_merchant = self.repo.create(
            data
        )


        return MerchantRegistrationResponse(

            message="Merchant registered successfully. Pending approval.",

            data=MerchantResponse(
                **new_merchant.to_response()
            ),

            success=True

        )