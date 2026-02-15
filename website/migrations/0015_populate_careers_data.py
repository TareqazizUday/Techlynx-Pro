# Generated migration for populating careers page data

from django.db import migrations


def populate_careers_data(apps, schema_editor):
    """Populate initial data for careers page"""
    CareersHero = apps.get_model('website', 'CareersHero')
    CareersStat = apps.get_model('website', 'CareersStat')
    JobDepartment = apps.get_model('website', 'JobDepartment')
    JobLocation = apps.get_model('website', 'JobLocation')
    JobOpening = apps.get_model('website', 'JobOpening')
    TalentManagement = apps.get_model('website', 'TalentManagement')
    TalentFeature = apps.get_model('website', 'TalentFeature')
    
    # Create Careers Hero
    CareersHero.objects.create(
        badge_text="Now Hiring: 12 Open Roles",
        headline='Build the Future or <span class="text-primary">Become the Face</span>',
        subheadline="Join our elite team of developers and marketers driving global innovation, or receive world-class management for your talent brand.",
        cta_primary_text="View Open Roles",
        cta_primary_url="#open-roles",
        cta_secondary_text="Get Represented",
        cta_secondary_url="#talent-services",
        testimonial_text="Working here felt like joining a family of geniuses.",
        testimonial_author="Sarah J., Senior Fullstack Engineer",
        is_active=True
    )
    
    # Create Career Stats
    stats_data = [
        {"number": "50+", "label": "Brands Partnered", "order": 1},
        {"number": "100+", "label": "Talent Placed", "order": 2},
        {"number": "12M+", "label": "Audience Reach", "order": 3},
        {"number": "98%", "label": "Success Rate", "order": 4},
    ]
    for stat in stats_data:
        CareersStat.objects.create(**stat, is_active=True)
    
    # Create Job Departments
    departments_data = [
        {"name": "Engineering", "slug": "engineering", "order": 1},
        {"name": "Marketing", "slug": "marketing", "order": 2},
        {"name": "Design", "slug": "design", "order": 3},
        {"name": "Product Management", "slug": "product-management", "order": 4},
    ]
    department_objects = {}
    for dept in departments_data:
        department_objects[dept['name']] = JobDepartment.objects.create(**dept, is_active=True)
    
    # Create Job Locations
    locations_data = [
        {"name": "Remote", "slug": "remote", "order": 1},
        {"name": "New York, NY", "slug": "new-york-ny", "order": 2},
        {"name": "Los Angeles, CA", "slug": "los-angeles-ca", "order": 3},
        {"name": "Hybrid (NYC)", "slug": "hybrid-nyc", "order": 4},
        {"name": "Hybrid (LA)", "slug": "hybrid-la", "order": 5},
    ]
    location_objects = {}
    for loc in locations_data:
        location_objects[loc['name']] = JobLocation.objects.create(**loc, is_active=True)
    
    # Create Job Openings
    jobs_data = [
        {
            "title": "Senior React Developer",
            "slug": "senior-react-developer",
            "department": department_objects["Engineering"],
            "location": location_objects["Remote"],
            "job_type": "full-time",
            "salary_range": "$140k - $180k",
            "description": "We're seeking an experienced React developer to build cutting-edge web applications.",
            "requirements": "5+ years of React experience, TypeScript proficiency, strong problem-solving skills.",
            "order": 1,
        },
        {
            "title": "Marketing Strategist",
            "slug": "marketing-strategist",
            "department": department_objects["Marketing"],
            "location": location_objects["New York, NY"],
            "job_type": "full-time",
            "salary_range": "$90k - $120k",
            "description": "Drive marketing campaigns and strategy for our growing client base.",
            "requirements": "3+ years marketing experience, data-driven mindset, creative thinking.",
            "order": 2,
        },
        {
            "title": "Talent Scout - Influencer Relations",
            "slug": "talent-scout-influencer-relations",
            "department": department_objects["Marketing"],
            "location": location_objects["Los Angeles, CA"],
            "job_type": "full-time",
            "salary_range": "$70k + Commission",
            "description": "Identify and onboard top influencer talent to our management roster.",
            "requirements": "Experience in talent management, strong network, excellent communication.",
            "order": 3,
        },
        {
            "title": "UI/UX Designer",
            "slug": "ui-ux-designer",
            "department": department_objects["Design"],
            "location": location_objects["Remote"],
            "job_type": "full-time",
            "salary_range": "$95k - $130k",
            "description": "Create beautiful, user-centered designs for web and mobile applications.",
            "requirements": "4+ years design experience, Figma expertise, portfolio required.",
            "order": 4,
        },
        {
            "title": "Product Manager",
            "slug": "product-manager",
            "department": department_objects["Product Management"],
            "location": location_objects["Hybrid (NYC)"],
            "job_type": "full-time",
            "salary_range": "$120k - $160k",
            "description": "Lead product strategy and development for our core platforms.",
            "requirements": "5+ years PM experience, technical background, stakeholder management.",
            "order": 5,
        },
    ]
    for job in jobs_data:
        JobOpening.objects.create(**job, is_active=True)
    
    # Create Talent Management
    TalentManagement.objects.create(
        headline="Scale Your Personal Brand Beyond Limits",
        description="We represent the next generation of culture-shapers. Our managers don't just find deals; they build legacies through strategic PR, legal protection, and blue-chip brand partnerships.",
        cta_text="Apply for Representation",
        cta_url="#application-form",
        is_active=True
    )
    
    # Create Talent Features
    features_data = [
        {
            "icon": "handshake",
            "title": "Contract Negotiation",
            "description": "Securing maximum value and long-term ownership for your content.",
            "order": 1,
        },
        {
            "icon": "trending_up",
            "title": "Brand Growth Strategy",
            "description": "Cross-platform optimization and performance-based marketing.",
            "order": 2,
        },
        {
            "icon": "campaign",
            "title": "Crisis PR & Legal",
            "description": "Proactive image management and round-the-clock legal advisory.",
            "order": 3,
        },
    ]
    for feature in features_data:
        TalentFeature.objects.create(**feature, is_active=True)


def reverse_func(apps, schema_editor):
    """Remove all careers data"""
    CareersHero = apps.get_model('website', 'CareersHero')
    CareersStat = apps.get_model('website', 'CareersStat')
    JobDepartment = apps.get_model('website', 'JobDepartment')
    JobLocation = apps.get_model('website', 'JobLocation')
    JobOpening = apps.get_model('website', 'JobOpening')
    TalentManagement = apps.get_model('website', 'TalentManagement')
    TalentFeature = apps.get_model('website', 'TalentFeature')
    
    CareersHero.objects.all().delete()
    CareersStat.objects.all().delete()
    JobOpening.objects.all().delete()
    JobDepartment.objects.all().delete()
    JobLocation.objects.all().delete()
    TalentManagement.objects.all().delete()
    TalentFeature.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0014_careershero_careersstat_jobdepartment_joblocation_and_more'),
    ]

    operations = [
        migrations.RunPython(populate_careers_data, reverse_func),
    ]
