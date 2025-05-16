from django.core.management.base import BaseCommand
from octofit_tracker.test_data import test_data
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from datetime import timedelta

class Command(BaseCommand):
    help = 'Populate the MongoDB database with test data for OctoFit Tracker.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Clearing existing data...'))
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Inserting users...'))
        user_objs = {}
        for user in test_data['users']:
            obj = User.objects.create(**user)
            user_objs[user['username']] = obj

        self.stdout.write(self.style.SUCCESS('Inserting teams...'))
        for team in test_data['teams']:
            members = [user_objs[username] for username in team['members']]
            team_obj = Team.objects.create(name=team['name'])
            team_obj.members = members
            team_obj.save()

        self.stdout.write(self.style.SUCCESS('Inserting activities...'))
        for activity in test_data['activities']:
            Activity.objects.create(
                user=user_objs[activity['user']],
                activity_type=activity['activity_type'],
                duration=timedelta(minutes=activity['duration'])
            )

        self.stdout.write(self.style.SUCCESS('Inserting leaderboard...'))
        for entry in test_data['leaderboard']:
            Leaderboard.objects.create(
                user=user_objs[entry['user']],
                score=entry['score']
            )

        self.stdout.write(self.style.SUCCESS('Inserting workouts...'))
        for workout in test_data['workouts']:
            Workout.objects.create(**workout)

        self.stdout.write(self.style.SUCCESS('Database population complete.'))
