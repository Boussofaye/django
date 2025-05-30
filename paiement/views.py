import json
import requests
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def initier_paiement(request):
    if request.method != "POST":
        return JsonResponse({"error": "Méthode non autorisée"}, status=405)

    try:
        data_request = json.loads(request.body)
        item_name = data_request.get("item_name", "Article sans nom")
        item_price = data_request.get("item_price", 1000)

        url = "https://app.paydunya.com/api/v1/checkout-invoice/create"

        # Attention : pas d'espace à la fin des URLs
        base_url="https://django-1-sewb.onrender.com"

        headers = {
            "Content-Type": "application/json",
            "PAYDUNYA-MASTER-KEY": settings.PAYDUNYA_MASTER_KEY,
            "PAYDUNYA-PRIVATE-KEY": settings.PAYDUNYA_PRIVATE_KEY,
            "PAYDUNYA-PUBLIC-KEY": settings.PAYDUNYA_PUBLIC_KEY,
            "PAYDUNYA-TOKEN": settings.PAYDUNYA_TOKEN,
        }

        montant = int(float(item_price))

        data = {
            "invoice": {
                "items": [
                    {
                        "name": item_name,
                        "quantity": 1,
                        "unit_price": montant
                    }
                ],
                "total_amount": montant,
                "description": f"Achat de {item_name}"
            },
            "store": {
                "name": "Ma Boutique",
                "tagline": "La satisfaction avant tout",
                "postal_address": "Dakar, Sénégal",
                "phone": "771234567"
            },
            "actions": {
                "cancel_url": f"{base_url}/paiement/fail/",
                "return_url": f"{base_url}/paiement/success/",
                "callback_url": f"{base_url}/paiement/callback/"
            }
        }

        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()

        # Debug : afficher la réponse PayDunya dans la console serveur
        print("Réponse PayDunya:", json.dumps(result, indent=2, ensure_ascii=False))

        if result.get("response_code") == "00":
            redirect_url = result.get("response", {}).get("checkout_url")
            if redirect_url:
                return JsonResponse({"redirect_url": redirect_url})
            else:
                return JsonResponse({"error": "URL de redirection manquante", "details": result}, status=500)
        else:
            return JsonResponse({"error": "Erreur PayDunya", "details": result}, status=500)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def paiement_success(request):
    return HttpResponse("✅ Paiement effectué avec succès. Merci pour votre achat.")


def paiement_fail(request):
    return HttpResponse("❌ Paiement annulé ou échoué. Veuillez réessayer.")


@csrf_exempt
def paiement_callback(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print("📩 Notification PayDunya reçue :", data)
            # TODO : enregistrer la transaction dans la base de données ici
            return JsonResponse({"status": "ok"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Méthode non autorisée"}, status=405)