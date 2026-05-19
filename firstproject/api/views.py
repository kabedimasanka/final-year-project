from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def battery_swap(request):
    
    print(request.data)  # 👈 ADD IT HERE

    code = request.data.get("code")

    if not code:
        return Response({"status": "failed", "message": "Code required"})

    if not code.isdigit() or len(code) != 6:
        return Response({
            "status": "failed",
            "message": "Code must be a 6-digit number"
        })

    if code == "123456":
        return Response({
            "status": "success",
            "battery": "released"
        })

    return Response({
        "status": "failed",
        "message": "Invalid code"
    })