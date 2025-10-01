from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils import Scrape
from .serializers import ProductSerializer

@api_view(['GET'])
def scrape_products(request):
    search = request.GET.get('search', 'iphone')
    items = int(request.GET.get('items', 5))

    scraper = Scrape.start(search=search, items=items)
    df = scraper.get_data()
    data = df.to_dict(orient='records')

    serializer = ProductSerializer(data=data, many=True)
    serializer.is_valid()  # چون داده‌ها خودمون درست کردیم، همیشه True میشه

    return Response(serializer.data)
