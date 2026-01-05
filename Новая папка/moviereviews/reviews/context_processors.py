from .models import Review

def latest_reviews(request):
    return {
        'latest_reviews': Review.objects.select_related('film', 'author')
        .order_by('-created_at')[:5]
    }