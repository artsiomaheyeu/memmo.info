import base64, io, hashlib, secrets
import qrcode

def generate_stable_id() -> str:
    """
    Короткий URL-safe ID. Не зависит от текста (поэтому может сохраняться при апдейте).
    """
    # 12 случайных байт → ~16 символов в base64-url без паддинга
    return base64.urlsafe_b64encode(secrets.token_bytes(12)).decode().rstrip("=")

def compute_content_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def make_qr_base64(url: str) -> str:
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=8, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image()
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("ascii")
