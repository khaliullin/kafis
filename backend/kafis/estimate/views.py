from rest_framework import serializers, status
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView

from estimate.models import Photo


class PhotoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Photo
        fields = ['name', 'gender', 'image']


class PhotoUploadView(APIView):
    parser_class = FileUploadParser,

    def get(self, request, *args, **kwargs):
        posts = Photo.objects.all()
        serializer = PhotoSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        path = 'no path'
        try:
            print('request.data:', request.data)
            serializer = PhotoSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                print('serializer.data', serializer.data)
                from estimate.core import process
                path = '/home/ubuntu/project/kafis/backend/kafis' + serializer.data['image']
                print(path)
                img_path, cls_name = process.preprocess(path,
                                             serializer.data['gender'],
                                             serializer.data['name'])
                # from PIL import Image
                # processed_image, cls_name = Image.open('estimate/core/certificate.jpg'), 'Вы прекрасны'
                # img_path = 'media/photos/certificate_999.jpg'.format(id)
                # processed_image.save(img_path)
                response = {
                    'image': img_path,
                    'result': cls_name
                }
                print(response)
                return Response(response, status=status.HTTP_201_CREATED)
            print('serializer not valid')
            raise AttributeError('No `name` or `gender` or `image` in', request.data)
        except Exception as e:
            print(str(e))
            return Response(str(e) + '\n' + path, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

