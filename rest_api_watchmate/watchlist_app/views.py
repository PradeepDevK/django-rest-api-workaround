# from django.shortcuts import render
# from watchlist_app.models import Movie
# from django.http import JsonResponse

# # Create your views here.
# def movie_list(request):
#     """
#     Complex Querysets -> Python Dictionary -> JSON Response
#     """
#     movies = Movie.objects.all()
#     data = {
#         'movies': list(movies.values()),
#     }
    
#     return JsonResponse(data)

# def movie_details(request, pk=None):
#     """
#     Complex Querysets -> Python Dictionary -> JSON Response
#     """
#     movie = Movie.objects.get(pk=pk)
#     data = {
#         'name': movie.name,
#         'description': movie.description,
#         'active': movie.active
#     }
    
#     return JsonResponse(data)