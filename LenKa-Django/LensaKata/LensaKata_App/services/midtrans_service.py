import midtransclient
from django.conf import settings


def create_payment_transaction(order_id, amount):
    """Fungsi untuk membuat transaksi menggunakan Midtrans Sandbox."""
    try:
        # Inisialisasi client Midtrans
        midtrans_client = midtransclient.Snap(
            is_production=False,
            server_key=settings.MIDTRANS_SERVER_KEY,
            client_key=settings.MIDTRANS_CLIENT_KEY
        )

        # Membuat transaksi
        transaction_response = midtrans_client.create_transaction({
            "transaction_details": {
                "order_id": order_id,
                "gross_amount": amount,
            },
            "customer_details": {
                "email": "user@example.com",
            },
            "callbacks": {
                "finish": "http://127.0.0.1:8000/payment-success/"
            }
        })

        return transaction_response.get("redirect_url")
    except Exception as e:
        return {"error": str(e)}
