from .models import Brand

def brands(request):
    """
    Context processor to specific brands to the templates.
    """
    brands = Brand.objects.all()
    return {'brands': brands}
