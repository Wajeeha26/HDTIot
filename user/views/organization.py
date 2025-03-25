from accounts.models.organization_model import Organization
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class OrganizationAPIView(APIView):

    def get(self, request, pk=None):
        if pk:
            organization = get_object_or_404(Organization, pk=pk)
            data = {
                "id": organization.id,
                "name": organization.name,
                "description": organization.description,
                "industry": organization.industry,
                "website": organization.website,
                "email": organization.email,
                "phone_number": organization.phone_number,
                "address": organization.address,
                "status": organization.status,
                "owner": organization.owner.id if organization.owner else None,
                "created_at": organization.created_at,
                "updated_at": organization.updated_at,
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            organizations = Organization.objects.all()
            data = [
                {
                    "id": org.id,
                    "name": org.name,
                    "description": org.description,
                    "industry": org.industry,
                    "website": org.website,
                    "email": org.email,
                    "phone_number": org.phone_number,
                    "address": org.address,
                    "status": org.status,
                    "owner": org.owner.id if org.owner else None,
                    "created_at": org.created_at,
                    "updated_at": org.updated_at,
                }
                for org in organizations
            ]
            return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data

        owner = request.user if request.user.is_authenticated else None

        organization = Organization.objects.create(
            name=data.get("name"),
            description=data.get("description"),
            industry=data.get("industry"),
            website=data.get("website"),
            email=data.get("email"),
            phone_number=data.get("phone_number"),
            address=data.get("address"),
            status=data.get("status"),
            owner=owner,
        )
        return Response(
            {
                "id": organization.id,
                "name": organization.name,
                "status": organization.status,
            },
            status=status.HTTP_201_CREATED,
        )

    def put(self, request, pk):
        organization = get_object_or_404(Organization, pk=pk)

        data = request.data
        organization.name = data.get("name", organization.name)
        organization.description = data.get("description", organization.description)
        organization.industry = data.get("industry", organization.industry)
        organization.website = data.get("website", organization.website)
        organization.email = data.get("email", organization.email)
        organization.phone_number = data.get("phone_number", organization.phone_number)
        organization.address = data.get("address", organization.address)
        organization.status = data.get("status", organization.status)

        organization.save()

        return Response(
            {
                "id": organization.id,
                "name": organization.name,
                "status": organization.status,
            },
            status=status.HTTP_200_OK,
        )

    def patch(self, request, pk):
        organization = get_object_or_404(Organization, pk=pk)

        data = request.data
        if "name" in data:
            organization.name = data["name"]
        if "description" in data:
            organization.description = data["description"]
        if "industry" in data:
            organization.industry = data["industry"]
        if "website" in data:
            organization.website = data["website"]
        if "email" in data:
            organization.email = data["email"]
        if "phone_number" in data:
            organization.phone_number = data["phone_number"]
        if "address" in data:
            organization.address = data["address"]
        if "status" in data:
            organization.status = data["status"]

        organization.save()

        return Response(
            {
                "id": organization.id,
                "name": organization.name,
                "status": organization.status,
            },
            status=status.HTTP_200_OK,
        )

    def delete(self, request, pk):
        organization = get_object_or_404(Organization, pk=pk)

        organization.delete()
        return Response(
            {"message": "Organization deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
