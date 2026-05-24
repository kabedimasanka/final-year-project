from rest_framework.decorators import api_view
from rest_framework.response import Response

from members.models import Reservation


@api_view(["POST"])
def battery_swap(request):
    code = request.data.get("code")

    if not code:
        return Response({"status": "failed", "message": "Code required"})

    if not code.isdigit() or len(code) != 6:
        return Response({
            "status": "failed",
            "message": "Code must be a 6-digit number",
        })

    reservation = Reservation.objects.filter(code=code).first()

    if not reservation:
        return Response({
            "status": "failed",
            "message": "Invalid code",
        })

    if reservation.status == "cancelled":
        return Response({
            "status": "failed",
            "message": "Reservation is cancelled",
        })

    return Response({
        "status": "success",
        "battery": "released",
        "reservation_id": reservation.id,
        "user_name": reservation.user_name,
        "reservation_status": reservation.status,
    })
