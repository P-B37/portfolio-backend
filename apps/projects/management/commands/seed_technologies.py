from django.core.management.base import BaseCommand
from apps.projects.models import Technology


class Command(BaseCommand):
    help = "Seed the database with professional technology tags for Network Engineering & Software Development"

    def handle(self, *args, **options):
        # Tailored tags for Network & Software Engineer
        tech_data = [
            # 1. Automation & IaC
            {"name": "Ansible", "category": "Automation", "icon_name": "ansible"},
            {"name": "Terraform", "category": "Automation", "icon_name": "terraform"},
            {"name": "Netmiko", "category": "Automation", "icon_name": "python"},
            {"name": "Nornir", "category": "Automation", "icon_name": "python"},
            {"name": "NAPALM", "category": "Automation", "icon_name": "python"},
            
            # 2. Networking & Infrastructure
            {"name": "Cisco IOS/NX-OS", "category": "Networking", "icon_name": "cisco"},
            {"name": "Juniper Junos", "category": "Networking", "icon_name": "juniper"},
            {"name": "BGP / OSPF", "category": "Networking", "icon_name": "network"},
            {"name": "EVE-NG", "category": "Networking", "icon_name": "network-virtual"},
            {"name": "GNS3", "category": "Networking", "icon_name": "network-virtual"},
            {"name": "VyOS", "category": "Networking", "icon_name": "linux"},
            {"name": "Wireshark", "category": "Networking", "icon_name": "wireshark"},

            # 3. Systems & Cloud (DevOps)
            {"name": "Docker", "category": "DevOps", "icon_name": "docker"},
            {"name": "Kubernetes", "category": "DevOps", "icon_name": "kubernetes"},
            {"name": "Proxmox", "category": "DevOps", "icon_name": "server"},
            {"name": "Linux (Ubuntu/Debian)", "category": "DevOps", "icon_name": "linux"},
            {"name": "Prometheus", "category": "DevOps", "icon_name": "prometheus"},
            {"name": "Grafana", "category": "DevOps", "icon_name": "grafana"},
            {"name": "AWS", "category": "DevOps", "icon_name": "aws"},

            # 4. Software Development
            {"name": "Python", "category": "Development", "icon_name": "python"},
            {"name": "Go (Golang)", "category": "Development", "icon_name": "go"},
            {"name": "Django", "category": "Development", "icon_name": "django"},
            {"name": "FastAPI", "category": "Development", "icon_name": "fastapi"},
            {"name": "React", "category": "Development", "icon_name": "react"},
            {"name": "Next.js", "category": "Development", "icon_name": "nextjs"},
            {"name": "PostgreSQL", "category": "Development", "icon_name": "postgresql"},
        ]

        created_count = 0
        updated_count = 0

        for item in tech_data:
            tech, created = Technology.objects.update_or_create(
                name=item["name"],
                defaults={
                    "category": item["category"],
                    "icon_name": item["icon_name"],
                }
            )
            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully seeded technologies! Created: {created_count}, Updated: {updated_count}"
            )
        )
