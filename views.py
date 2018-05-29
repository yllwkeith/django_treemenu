from django.shortcuts import render


# Create your views here.
def index(request):
    print(request)
    return render(request, 'index.html')


def stub_view(request, pk):
    print(request, pk)
    context = {'menu_item_id': pk}
    return render(request, 'index.html', context)
