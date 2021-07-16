from django import template
from stats.models import ChampionClassImage, ChampionImage
from django.template.defaultfilters import stringfilter

register = template.Library()

#image type must be 'champion_class_image' or 'champion_image' and name must be the class name or champion name

@stringfilter
def get_image_url(name, image_type):
    if image_type == 'champion_image':
        url_path = ChampionImage.objects.get(champion_name=name).image_url
    elif image_type == 'champion_class_image':
        url_path = ChampionClassImage.objects.get(champion_class_name=name).image_url
    return url_path

register.filter('get_image_url', get_image_url)

