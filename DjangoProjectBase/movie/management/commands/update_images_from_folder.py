import os
from django.core.management.base import BaseCommand
from django.conf import settings
from movie.models import Movie

class Command(BaseCommand):
    help = "Update movie images from media/movie/images folder"

    def handle(self, *args, **kwargs):
        # Path to your images folder
        images_path = os.path.join(settings.MEDIA_ROOT, "movie", "images")

        if not os.path.exists(images_path):
            self.stdout.write(self.style.ERROR(f"Path not found: {images_path}"))
            return

        updated_count = 0
        skipped_count = 0

        for filename in os.listdir(images_path):
            if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
                continue

            # Example: m_Carmencita.png → Carmencita
            name, _ = os.path.splitext(filename)
            clean_name = name.replace("m_", "").replace("_", " ").strip()

            try:
                movie = Movie.objects.get(title__iexact=clean_name)
                movie.image = f"movie/images/{filename}"
                movie.save()
                updated_count += 1
                self.stdout.write(self.style.SUCCESS(f"Updated image for {movie.title}"))
            except Movie.DoesNotExist:
                skipped_count += 1
                self.stdout.write(self.style.WARNING(f"No movie found for {clean_name}"))

        self.stdout.write(
            self.style.SUCCESS(
                f"Done! Updated {updated_count} movies, skipped {skipped_count}."
            )
        )
