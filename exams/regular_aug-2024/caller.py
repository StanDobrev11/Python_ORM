import os
import django
from django.db.models import Q, Count, Sum, Avg

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Astronaut, Mission, Spacecraft


# Create queries within functions
def get_astronauts(search_string=None):
    """It retrieves astronaut objects by partially and case-insensitively matching the given searching criteria for
    name or phone number. Check if any of these two field values contain the searched string."""

    if search_string is None:
        return ''

    query = Q(name__icontains=search_string) | Q(phone_number__icontains=search_string)
    astronauts = Astronaut.objects.filter(query).order_by('name')

    if astronauts.exists():
        return '\n'.join(
            f"Astronaut: {astronaut.name}, phone number: {astronaut.phone_number}, status: {'Active' if astronaut.is_active else 'Inactive'}"
            for astronaut in astronauts
        )
    else:
        return ''


def get_top_astronaut():
    """It retrieves the astronaut with the greatest number of participated missions."""
    if not Astronaut.objects.exists() or not Mission.objects.exists():
        return 'No data.'

    top_astro = Astronaut.objects.get_astronauts_by_missions_count().first()

    if top_astro and top_astro.missions_count > 0:
        return f"Top Astronaut: {top_astro.name} with {top_astro.missions_count} missions."
    else:
        return 'No data.'


def get_top_commander():
    """It retrieves the astronaut with the greatest number of commanded missions."""
    if not Astronaut.objects.exists() or not Mission.objects.exists():
        return 'No data.'

    top_commander = Astronaut.objects.annotate(
        commanded_missions=Count('commander')
    ).order_by('-commanded_missions', 'phone_number').first()

    if top_commander and top_commander.commanded_missions > 0:
        return f"Top Commander: {top_commander.name} with {top_commander.commanded_missions} commanded missions."
    else:
        return 'No data.'


def get_last_completed_mission():
    """It retrieves information about the last completed mission (latest launch date and mission status "Completed")
    and returns a string in the following format:"""

    last_mission = (Mission.objects
                    .filter(status='Completed')
                    .order_by('-launch_date')
                    .select_related('spacecraft', 'commander')
                    .prefetch_related('astronauts')
                    .first())

    if not last_mission:
        return "No data."

    astronauts = last_mission.astronauts.all().order_by('name')
    astronaut_names = ', '.join(astronaut.name for astronaut in astronauts)
    total_spacewalks = astronauts.aggregate(Sum('spacewalks'))['spacewalks__sum'] or 0

    return (f"The last completed mission is: {last_mission.name}. "
            f"Commander: {last_mission.commander.name if last_mission.commander else 'TBA'}. "
            f"Astronauts: {astronaut_names}. "
            f"Spacecraft: {last_mission.spacecraft.name}. "
            f"Total spacewalks: {total_spacewalks}.")


def get_most_used_spacecraft():
    """It retrieves the most used spacecraft by considering the number of missions it was assigned to.
    If you have spacecrafts used in the same number of missions, order them by spacecraft's name ascending,
    and get the first one."""

    if not Mission.objects.exists():
        return "No data."

    spacecraft = (Spacecraft.objects
                  .annotate(missions_count=Count('missions'))
                  .order_by('-missions_count', 'name')
                  .first())

    if not spacecraft or spacecraft.missions_count == 0:
        return "No data."

    astronauts_count = (
        Mission.objects.filter(spacecraft=spacecraft)
        .aggregate(astronauts_count=Count('astronauts', distinct=True))['astronauts_count'])

    return (f"The most used spacecraft is: {spacecraft.name}, "
            f"manufactured by {spacecraft.manufacturer}, "
            f"used in {spacecraft.missions_count} missions, "
            f"astronauts on missions: {astronauts_count}.")


def decrease_spacecrafts_weight():
    """It filters the unique spacecraft objects currently assigned to planned missions (mission status "Planned")
    and decreases their weight by 200.0 kilograms.
    The spacecraft's weight should not drop below zero(0.0), therefore filter further only those objects that weigh at
    least 200.0 kg.
    Decrease the weight only once if the spacecraft participates in multiple planned missions.
    """

    spacecrafts = Spacecraft.objects.filter(missions__status='Planned', weight__gte=200.0).distinct()

    for craft in spacecrafts:
        craft.weight -= 200
        craft.save()

    if not spacecrafts:
        return "No changes in weight."

    avg_weight = Spacecraft.objects.aggregate(avg_weight=Avg('weight'))['avg_weight']

    return (f"The weight of {spacecrafts.count()} spacecrafts has been decreased. "
            f"The new average weight of all spacecrafts is {avg_weight}kg")


if __name__ == '__main__':
    print(get_last_completed_mission())
    # print(get_most_used_spacecraft())
    # print(decrease_spacecrafts_weight())
