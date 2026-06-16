import os
import flet as ft
import flet_video as ftv
import webbrowser
import threading

def main(page: ft.Page):

    # =========================================================
    # PAGE SETTINGS (Optimized for Fixed Header Layout)
    # =========================================================
    page.title = "Mweutota N Lukas - Mining Engineering Portfolio | MechTek Developer"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.spacing = 0
    page.bgcolor = "#f0f7ff"
    page.scroll = None

    # =========================================================
    # MODERN MINING ENGINEERING PALETTE (Blue/Teal/Slate)
    # =========================================================
    PRIMARY_BLUE = "#1a5f7a"           # Deep Mining Blue
    ACCENT_TEAL = "#2c8c6e"            # Safety Green/Teal
    DEEP_SLATE = "#2c3e50"             # Dark slate for text/buttons
    LIGHT_BG = "#f0f7ff"               # Light blue-tint background
    SECTION_BLUE = "#e3f0f5"
    SECTION_DEEP = "#cde5ef"
    BG_WHITE = "#ffffff"
    TEXT_GREY = "#3a5a6e"
    AVATAR_BG = "#e3f0f5"
    SUBTEXT_GREY = "#6b8da8"
    CARD_BG = "#fafeff"
    BORDER_COLOR = "#b8d4e3"
    
    DARK_CARD_BG = "#1a5f7a"
    DARK_TEXT_WHITE = "#ffffff"
    NAV_INACTIVE = "#c5dce8"
    OVERLAY_TEAL = "#2c8c6e"
    PROGRESS_TRACK = "#e3f0f5"
    SHADOW_BLUE = "#b8d4e3"
    CERT_HINT = "#c5dce8"

    # Image mapping based on available assets
    IMAGES = {
        "profile": "/images/Profile.jpeg",
        "matlab_onramp": "/images/MATLAB Onramp.jpeg",
        "simulink_onramp": "/images/Simulink Onramp.jpeg",
        "machine_learning": "/images/Machine Learning Onramp.jpeg",
        "reinforcement_learning": "/images/Reinforcement Learning Onramp.jpeg",
        "calculations_vectors": "/images/Calculations with Vectors and Matrices.jpeg",
        "explore_data": "/images/Explore Data with MATLAB Plots.jpeg",
        "make_matrices": "/images/Make and Manipulate Matrices.jpeg",
    }

    # Global variable to track active dialog
    active_dialog = None

    def open_certificate_zoom(title: str, image_file: str):
        global active_dialog
        
        # Create dialog content
        zoom_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(title, color=PRIMARY_BLUE, weight=ft.FontWeight.BOLD),
            content=ft.Container(
                width=900,
                height=620,
                bgcolor=BG_WHITE,
                padding=10,
                border_radius=8,
                content=ft.Image(src=image_file, fit="contain"),
            ),
            actions=[
                ft.TextButton(
                    "Close", 
                    on_click=lambda e: close_certificate_zoom(),
                    style=ft.ButtonStyle(color=PRIMARY_BLUE)
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        active_dialog = zoom_dialog
        page.show_dialog(zoom_dialog)
        page.update()

    def close_certificate_zoom():
        global active_dialog
        if active_dialog:
            active_dialog.open = False
            active_dialog.update()
            active_dialog = None

    def get_uniform_border(width: int, color: str):
        return ft.Border(
            top=ft.BorderSide(width, color),
            bottom=ft.BorderSide(width, color),
            left=ft.BorderSide(width, color),
            right=ft.BorderSide(width, color),
        )

    # =========================================================
    # PREMIUM COMPONENT BUILDERS
    # =========================================================
    def create_section_header(title: str, subtitle: str):
        return ft.Column(
            spacing=8,
            controls=[
                ft.Text(
                    title, 
                    size=28, 
                    weight=ft.FontWeight.BOLD, 
                    color=PRIMARY_BLUE, 
                    style=ft.TextStyle(letter_spacing=1.2)
                ),
                ft.Text(subtitle, size=15, color=TEXT_GREY),
                ft.Container(height=4, width=60, bgcolor=ACCENT_TEAL, border_radius=2),
                ft.Container(height=15)
            ]
        )

    def create_skill_chip(label: str, level: float):
        return ft.Container(
            bgcolor=BG_WHITE,
            padding=ft.Padding(16, 12, 16, 12),
            border_radius=8,
            border=get_uniform_border(1, BORDER_COLOR),
            content=ft.Column([
                ft.Row([
                    ft.Text(label, weight=ft.FontWeight.W_600, color=DEEP_SLATE, size=14),
                    ft.Text(f"{int(level*100)}%", weight=ft.FontWeight.BOLD, color=PRIMARY_BLUE, size=12)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Container(height=6),
                ft.Stack([
                    ft.Container(height=4, bgcolor=PROGRESS_TRACK, border_radius=2, expand=True),
                    ft.Container(height=4, bgcolor=PRIMARY_BLUE, border_radius=2, width=120 * level)
                ])
            ])
        )

    def create_info_card(title: str, body: str, icon=ft.Icons.CHECK_CIRCLE):
        return ft.Container(
            bgcolor=BG_WHITE,
            padding=20,
            border_radius=8,
            border=get_uniform_border(1, BORDER_COLOR),
            content=ft.Column(
                spacing=10,
                controls=[
                    ft.Row([
                        ft.Icon(icon, color=PRIMARY_BLUE, size=24),
                        ft.Text(title, size=16, weight=ft.FontWeight.BOLD, color=DEEP_SLATE),
                    ]),
                    ft.Text(body, color=TEXT_GREY, size=13),
                ],
            ),
        )

    # =========================================================
    # NAVIGATION SYSTEM
    # =========================================================
    current_page_key = {"value": "overview"}
    nav_buttons = {}

    def build_page_view(section_control, page_key):
        return ft.Column(
            key=f"page-{page_key}",
            expand=True,
            scroll=ft.ScrollMode.ALWAYS,
            spacing=0,
            controls=[section_control],
        )

    def navigate_to(page_key):
        current_page_key["value"] = page_key
        page_switcher.content = build_page_view(portfolio_pages[page_key], page_key)
        for key, button in nav_buttons.items():
            button.style = ft.ButtonStyle(
                color=BG_WHITE if key == page_key else NAV_INACTIVE,
                overlay_color=OVERLAY_TEAL,
            )
        page.update()

    # =========================================================
    # SECTIONS DEFINITIONS
    # =========================================================
    
    # 1. Overview Section
    hero_section = ft.Container(
        key="overview",
        bgcolor=LIGHT_BG,
        padding=ft.Padding(50, 60, 50, 60),
        content=ft.ResponsiveRow(
            controls=[
                ft.Column(
                    col={"sm": 12, "md": 7},
                    spacing=15,
                    controls=[
                        ft.Text(
                            "MINING ENGINEERING STUDENT @ UNAM ONGWEDIVA CAMPUS", 
                            size=13, 
                            weight=ft.FontWeight.W_600, 
                            color=ACCENT_TEAL, 
                            style=ft.TextStyle(letter_spacing=1.5)
                        ),
                        ft.Text("Mweutota N Lukas", size=42, weight=ft.FontWeight.BOLD, color=PRIMARY_BLUE),
                        ft.Text("Student Number: 224066656", size=16, weight=ft.FontWeight.W_500, color=ACCENT_TEAL),
                        ft.Text("Student Developer | MechTek Developer", size=14, color=TEXT_GREY, italic=True),
                        ft.Divider(color=PRIMARY_BLUE, thickness=1.5),
                        ft.Text("Phone: +264 81 784 8256  |  Email: lukasmweutota02@gmail.com", size=14, weight=ft.FontWeight.W_500, color=DEEP_SLATE),
                        ft.Text("GitHub: mweutotalucky-prog", size=14, weight=ft.FontWeight.W_500, color=DEEP_SLATE),
                        ft.Text("Mining Engineering student with expertise in React Native, Firebase, and MATLAB. I develop mobile applications that solve real-world engineering problems. This portfolio documents my contributions to the MechTek project - a fault reporting and maintenance tracking system.", size=16, color=TEXT_GREY),
                        ft.Container(height=10),
                        ft.ElevatedButton(
                            "Download CV (PDF)",
                            icon=ft.Icons.DOWNLOAD,
                            bgcolor=PRIMARY_BLUE,
                            color=BG_WHITE,
                            url="/Mweutota_N_Lukas_CV.pdf",
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=6)),
                        ),
                        ft.Container(height=5),
                        ft.TextButton(
                            "View GitHub Repository",
                            icon=ft.Icons.CODE,
                            url="https://github.com/mweutotalucky-prog",
                            style=ft.ButtonStyle(color=ACCENT_TEAL),
                        ),
                    ],
                ),
                ft.Column(
                    col={"sm": 12, "md": 5},
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Container(
                            width=280,
                            height=280,
                            border_radius=140,
                            bgcolor=AVATAR_BG,
                            alignment=ft.Alignment(0, 0),
                            border=get_uniform_border(4, PRIMARY_BLUE),
                            content=ft.Image(src=IMAGES["profile"], width=280, height=280, border_radius=140, fit="cover"),
                        ),
                        ft.Container(height=12),
                        ft.Text("Mining Engineering & Mine Safety Systems 2026", size=12, color=SUBTEXT_GREY, italic=True),
                        ft.Container(
                            content=ft.Row(
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=8,
                                controls=[
                                    ft.Icon(ft.Icons.SCHOOL, size=14, color=PRIMARY_BLUE),
                                    ft.Text("UNAM Ongwediva Engineering Campus", size=11, color=TEXT_GREY),
                                ]
                            )
                        ),
                    ],
                ),
            ]
        ),
    )

    # 2. Skills Section
    skills_section = ft.Container(
        key="skills",
        bgcolor=SECTION_BLUE,
        padding=40,
        content=ft.Column([
            create_section_header("TECHNICAL SKILLS MATRIX", "Integrated expertise across software development, mining engineering, and data analysis."),
            ft.ResponsiveRow([
                ft.Column(col={"sm": 12, "md": 4}, spacing=10, controls=[
                    ft.Text("Software Development", weight=ft.FontWeight.BOLD, color=ACCENT_TEAL, size=16),
                    create_skill_chip("JavaScript", 0.88),
                    create_skill_chip("React Native", 0.90),
                    create_skill_chip("Python", 0.82),
                    create_skill_chip("Firebase", 0.85),
                    create_skill_chip("HTML & CSS", 0.87),
                ]),
                ft.Column(col={"sm": 12, "md": 4}, spacing=10, controls=[
                    ft.Text("MATLAB & Data Analysis", weight=ft.FontWeight.BOLD, color=ACCENT_TEAL, size=16),
                    create_skill_chip("MATLAB", 0.92),
                    create_skill_chip("Simulink", 0.85),
                    create_skill_chip("Machine Learning (MATLAB)", 0.80),
                    create_skill_chip("Data Visualization", 0.88),
                    create_skill_chip("Matrix Computations", 0.90),
                ]),
                ft.Column(col={"sm": 12, "md": 4}, spacing=10, controls=[
                    ft.Text("Mining Engineering", weight=ft.FontWeight.BOLD, color=ACCENT_TEAL, size=16),
                    create_skill_chip("Mine Planning", 0.85),
                    create_skill_chip("Rock Mechanics", 0.82),
                    create_skill_chip("Ventilation Systems", 0.80),
                    create_skill_chip("Drilling & Blasting", 0.78),
                    create_skill_chip("Git & GitHub", 0.90),
                ]),
            ], spacing=20)
        ])
    )

    # 3. Individual Portfolio Reflection Section - MechTek Focus
    contribution_section = ft.Container(
        key="contribution",
        bgcolor=LIGHT_BG,
        padding=40,
        content=ft.Column(
            spacing=20,
            controls=[
                create_section_header("MECHTEK - FAULT REPORTING & MAINTENANCE SYSTEM", "Reflection, evidence, lessons learned, challenges, and showcase material."),
                ft.ResponsiveRow(
                    spacing=20,
                    run_spacing=20,
                    controls=[
                        ft.Container(
                            col={"sm": 12, "md": 6},
                            content=create_info_card(
                                "UI/UX Development",
                                "Designed and developed the complete user interface for the MechTek mobile application using React Native, focusing on intuitive navigation and seamless user experience.",
                                ft.Icons.DESIGN_SERVICES,
                            ),
                        ),
                        ft.Container(
                            col={"sm": 12, "md": 6},
                            content=create_info_card(
                                "Firebase Integration",
                                "Integrated Firebase Firestore for real-time data storage, Authentication for user management, and Cloud Storage for media attachments.",
                                ft.Icons.CLOUD_SYNC,
                            ),
                        ),
                        ft.Container(
                            col={"sm": 12, "md": 6},
                            content=create_info_card(
                                "Dashboard & Navigation",
                                "Built responsive dashboard views, implemented navigation state management, and optimized UI performance across different devices.",
                                ft.Icons.DASHBOARD,
                            ),
                        ),
                        ft.Container(
                            col={"sm": 12, "md": 6},
                            content=create_info_card(
                                "GitHub Management",
                                "Managed version control with Git/GitHub, conducted code reviews, and maintained repository structure for the project team.",
                                ft.Icons.CODE,
                            ),
                        ),
                    ],
                ),
                ft.Container(
                    bgcolor=LIGHT_BG,
                    padding=20,
                    border_radius=8,
                    border=get_uniform_border(1, BORDER_COLOR),
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Column([
                                ft.Text("Project Showcase", size=18, weight=ft.FontWeight.BOLD, color=DEEP_SLATE),
                                ft.Text("View the MechTek application in action with real-time fault reporting and maintenance tracking.", color=TEXT_GREY, size=13),
                            ]),
                            ft.TextButton("Watch Demo", icon=ft.Icons.PLAY_CIRCLE, url="https://example.com/mechtek-demo", style=ft.ButtonStyle(color=ACCENT_TEAL)),
                        ],
                    ),
                ),
            ],
        ),
    )

    # 4. Project Timeline Section
    timeline_section = ft.Container(
        key="timeline",
        bgcolor=LIGHT_BG,
        padding=40,
        content=ft.Column(
            spacing=20,
            controls=[
                create_section_header("MECHTEK PROJECT TIMELINE", "Development journey of the Fault Reporting & Maintenance Tracking System."),
                ft.Container(
                    bgcolor=BG_WHITE,
                    padding=25,
                    border_radius=10,
                    border=get_uniform_border(1, BORDER_COLOR),
                    content=ft.Column(
                        spacing=15,
                        controls=[
                            ft.Text("Phase 1: Requirements & Planning", size=18, weight=ft.FontWeight.BOLD, color=ACCENT_TEAL),
                            ft.Text("Gathered project requirements, defined user stories, and planned the application architecture for the MechTek fault reporting system.", color=TEXT_GREY),
                            ft.Divider(color=BORDER_COLOR),
                            ft.Text("Phase 2: UI/UX Design & Prototyping", size=18, weight=ft.FontWeight.BOLD, color=ACCENT_TEAL),
                            ft.Text("Designed the application interface, created wireframes and prototypes, and established the visual design language for the maintenance tracking system.", color=TEXT_GREY),
                            ft.Divider(color=BORDER_COLOR),
                            ft.Text("Phase 3: Frontend Development", size=18, weight=ft.FontWeight.BOLD, color=ACCENT_TEAL),
                            ft.Text("Implemented the React Native frontend, developed navigation flows, created dashboard views, and integrated UI components.", color=TEXT_GREY),
                            ft.Divider(color=BORDER_COLOR),
                            ft.Text("Phase 4: Firebase Integration", size=18, weight=ft.FontWeight.BOLD, color=ACCENT_TEAL),
                            ft.Text("Integrated Firebase services including Firestore database, Authentication, and Cloud Storage for seamless data management.", color=TEXT_GREY),
                            ft.Divider(color=BORDER_COLOR),
                            ft.Text("Phase 5: Testing & Optimization", size=18, weight=ft.FontWeight.BOLD, color=ACCENT_TEAL),
                            ft.Text("Conducted comprehensive testing, optimized UI performance, fixed navigation state issues, and prepared the application for deployment.", color=TEXT_GREY),
                        ],
                    ),
                ),
            ],
        ),
    )

    # 5. Projects Section
    project_section = ft.Container(
        key="projects",
        bgcolor=BG_WHITE,
        padding=40,
        content=ft.Column(
            spacing=20,
            controls=[
                create_section_header("MECHTEK - FAULT REPORTING & MAINTENANCE APP", "Core features and technical achievements."),
                ft.ResponsiveRow(
                    spacing=20,
                    run_spacing=20,
                    controls=[
                        ft.Container(
                            col={"sm": 12, "md": 6},
                            bgcolor=CARD_BG,
                            padding=25,
                            border_radius=10,
                            border=get_uniform_border(1, BORDER_COLOR),
                            content=ft.Column(
                                spacing=12,
                                controls=[
                                    ft.Text("1. Fault Reporting System", size=18, weight=ft.FontWeight.BOLD, color=ACCENT_TEAL),
                                    ft.Text("Mobile application for reporting equipment faults, tracking maintenance tasks, and managing repair workflows in real-time.", color=TEXT_GREY, size=14),
                                    ft.Container(
                                        bgcolor=LIGHT_BG,
                                        padding=12,
                                        border_radius=6,
                                        content=ft.Column([
                                            ft.Text("TECHNICAL SPECIFICATIONS:", size=11, weight=ft.FontWeight.BOLD, color=DEEP_SLATE),
                                            ft.Text("• Frontend: React Native with TypeScript", size=12, font_family="monospace", color=PRIMARY_BLUE),
                                            ft.Text("• Backend: Firebase Firestore DB", size=12, font_family="monospace", color=PRIMARY_BLUE),
                                            ft.Text("• Authentication: Firebase Auth", size=12, font_family="monospace", color=PRIMARY_BLUE),
                                            ft.Text("• Storage: Firebase Cloud Storage", size=12, font_family="monospace", color=PRIMARY_BLUE),
                                        ])
                                    ),
                                    ft.Text("Enables maintenance teams to log faults, track repair progress, and manage equipment maintenance schedules efficiently.", color=TEXT_GREY, size=12),
                                    ft.Row([
                                        ft.Container(content=ft.Text("React Native", size=11, color=BG_WHITE), bgcolor=PRIMARY_BLUE, padding=5, border_radius=4),
                                        ft.Container(content=ft.Text("Firebase", size=11, color=BG_WHITE), bgcolor=ACCENT_TEAL, padding=5, border_radius=4),
                                    ])
                                ],
                            ),
                        ),
                        ft.Container(
                            col={"sm": 12, "md": 6},
                            bgcolor=CARD_BG,
                            padding=25,
                            border_radius=10,
                            border=get_uniform_border(1, BORDER_COLOR),
                            content=ft.Column(
                                spacing=12,
                                controls=[
                                    ft.Text("2. Maintenance Tracking Dashboard", size=18, weight=ft.FontWeight.BOLD, color=ACCENT_TEAL),
                                    ft.Text("Interactive dashboard for monitoring maintenance activities, tracking repair status, and visualizing equipment health metrics.", color=TEXT_GREY, size=14),
                                    ft.Container(
                                        bgcolor=LIGHT_BG,
                                        padding=12,
                                        border_radius=6,
                                        content=ft.Column([
                                            ft.Text("DASHBOARD FEATURES:", size=11, weight=ft.FontWeight.BOLD, color=DEEP_SLATE),
                                            ft.Text("• Real-time status updates", size=12, font_family="monospace", color=PRIMARY_BLUE),
                                            ft.Text("• Equipment health monitoring", size=12, font_family="monospace", color=PRIMARY_BLUE),
                                            ft.Text("• Maintenance scheduling", size=12, font_family="monospace", color=PRIMARY_BLUE),
                                            ft.Text("• Reporting & analytics", size=12, font_family="monospace", color=PRIMARY_BLUE),
                                        ])
                                    ),
                                    ft.Text("Provides comprehensive visibility into maintenance operations with intuitive data visualization and reporting capabilities.", color=TEXT_GREY, size=12),
                                    ft.Row([
                                        ft.Container(content=ft.Text("Dashboard", size=11, color=BG_WHITE), bgcolor=PRIMARY_BLUE, padding=5, border_radius=4),
                                        ft.Container(content=ft.Text("Analytics", size=11, color=DEEP_SLATE), bgcolor=LIGHT_BG, padding=5, border_radius=4),
                                    ])
                                ],
                            ),
                        ),
                    ],
                ),
            ],
        ),
    )

    # 6. Technical Blog Section - WITH VIDEO
    blog_section = ft.Container(
        key="blog",
        bgcolor=LIGHT_BG,
        padding=40,
        content=ft.Column(
            spacing=20,
            controls=[
                create_section_header("TECHNICAL BLOG: MINING & SOFTWARE INSIGHTS", "Written technical explanations with embedded video demonstrations."),
                ft.ResponsiveRow(
                    spacing=20,
                    run_spacing=20,
                    controls=[
                        ft.Container(
                            col={"sm": 12, "md": 6},
                            bgcolor=BG_WHITE,
                            padding=22,
                            border_radius=8,
                            border=get_uniform_border(1, BORDER_COLOR),
                            content=ft.Column(
                                spacing=12,
                                controls=[
                                    ft.Text("MATLAB for Mining Engineering", size=18, weight=ft.FontWeight.BOLD, color=ACCENT_TEAL),
                                    ft.Text("MATLAB provides powerful computational tools for mining engineering applications including rock mechanics analysis, ventilation modeling, and mine planning optimization.", color=TEXT_GREY, size=13),
                                    ft.Container(
                                        bgcolor=LIGHT_BG,
                                        padding=14,
                                        border_radius=6,
                                        content=ft.Text("Rock Stress = f(Depth, Geology, Load)  |  Airflow = g(Network, Fans)", font_family="monospace", size=14, color=PRIMARY_BLUE),
                                    ),
                                    ft.Text("These computational models help mining engineers predict ground behavior, optimize ventilation systems, and improve operational safety.", color=TEXT_GREY, size=13),
                                ],
                            ),
                        ),
                        ft.Container(
                            col={"sm": 12, "md": 6},
                            bgcolor=BG_WHITE,
                            padding=22,
                            border_radius=8,
                            border=get_uniform_border(1, BORDER_COLOR),
                            content=ft.Column(
                                spacing=12,
                                controls=[
                                    ft.Text("Firebase for Mobile App Development", size=18, weight=ft.FontWeight.BOLD, color=ACCENT_TEAL),
                                    ft.Text("Firebase provides a complete backend solution for mobile applications with real-time database, authentication, and cloud storage capabilities.", color=TEXT_GREY, size=13),
                                    ft.Container(
                                        bgcolor=LIGHT_BG,
                                        padding=14,
                                        border_radius=6,
                                        content=ft.Text("Data Sync = Real-time Updates  |  Auth = Role-based Access", font_family="monospace", size=14, color=PRIMARY_BLUE),
                                    ),
                                    ft.Text("This architecture enables seamless data synchronization across devices, secure user authentication, and efficient media storage for fault reporting applications.", color=TEXT_GREY, size=13),
                                ],
                            ),
                        ),
                    ],
                ),
                # VIDEO SECTION - Embedded Video Player
                ft.Container(
                    padding=ft.Padding(0, 30, 0, 0),  # top=30, left=0, right=0, bottom=0
                    content=ft.Column(
                        spacing=15,
                        controls=[
                            ft.Divider(color=BORDER_COLOR, thickness=1),
                            ft.Text("📹 MECHTEK PROJECT DEMONSTRATION", size=20, weight=ft.FontWeight.BOLD, color=PRIMARY_BLUE, text_align=ft.TextAlign.CENTER),
                            ft.Text("Watch the full demonstration of the MechTek fault reporting and maintenance tracking system.", size=14, color=TEXT_GREY, text_align=ft.TextAlign.CENTER),
                            ft.Container(
                                padding=20,
                                bgcolor=BG_WHITE,
                                border_radius=12,
                                border=get_uniform_border(2, BORDER_COLOR),
                                content=ftv.Video(
                                    expand=True,
                                    playlist=[ftv.VideoMedia("/video/video.mp4")],
                                    playlist_mode=ftv.PlaylistMode.LOOP,
                                    fill_color=PRIMARY_BLUE,
                                    aspect_ratio=16/9,
                                    volume=100,
                                    autoplay=True,
                                    show_controls=True,
                                    filter_quality=ft.FilterQuality.HIGH,
                                    muted=False,
                                    wakelock=True,
                                ),
                            ),
                            ft.Text("This video showcases the key features, UI/UX design, and technical implementations of the MechTek application.", size=12, color=SUBTEXT_GREY, text_align=ft.TextAlign.CENTER, italic=True),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ),
            ],
        ),
    )

    # 7. Experience / Leadership Section
    leadership_section = ft.Container(
        key="experience",
        bgcolor=LIGHT_BG,
        padding=40,
        content=ft.Column(
            spacing=20,
            controls=[
                create_section_header("LEADERSHIP & PROJECT EXPERIENCE", "Active contributions to software development and engineering projects."),
                ft.Text("Combining mining engineering knowledge with software development skills to create practical solutions for the industry.", size=15, color=TEXT_GREY),
                ft.ResponsiveRow(
                    spacing=20,
                    controls=[
                        ft.Container(
                            col={"sm": 12, "md": 6},
                            bgcolor=BG_WHITE,
                            padding=20,
                            border_radius=8,
                            border=get_uniform_border(1, BORDER_COLOR),
                            content=ft.Column([
                                ft.Icon(ft.Icons.CODE, color=PRIMARY_BLUE, size=28),
                                ft.Text("React Native Developer", size=16, weight=ft.FontWeight.BOLD, color=DEEP_SLATE),
                                ft.Text("Developed the MechTek mobile application with cross-platform capabilities, ensuring seamless performance on both Android and iOS devices.", color=TEXT_GREY, size=13),
                                ft.Text("• Cross-platform mobile development", size=12, color=TEXT_GREY),
                                ft.Text("• State management with React Navigation", size=12, color=TEXT_GREY),
                            ])
                        ),
                        ft.Container(
                            col={"sm": 12, "md": 6},
                            bgcolor=BG_WHITE,
                            padding=20,
                            border_radius=8,
                            border=get_uniform_border(1, BORDER_COLOR),
                            content=ft.Column([
                                ft.Icon(ft.Icons.FIRE_EXTINGUISHER, color=PRIMARY_BLUE, size=28),
                                ft.Text("Firebase Backend Integration", size=16, weight=ft.FontWeight.BOLD, color=DEEP_SLATE),
                                ft.Text("Integrated Firebase services including Firestore database, Authentication, and Cloud Storage for seamless data management.", color=TEXT_GREY, size=13),
                                ft.Text("• Real-time data synchronization", size=12, color=TEXT_GREY),
                                ft.Text("• Role-based access control", size=12, color=TEXT_GREY),
                            ])
                        ),
                        ft.Container(
                            col={"sm": 12, "md": 6},
                            bgcolor=BG_WHITE,
                            padding=20,
                            border_radius=8,
                            border=get_uniform_border(1, BORDER_COLOR),
                            content=ft.Column([
                                ft.Icon(ft.Icons.DASHBOARD, color=PRIMARY_BLUE, size=28),
                                ft.Text("Dashboard & UI Design", size=16, weight=ft.FontWeight.BOLD, color=DEEP_SLATE),
                                ft.Text("Created responsive dashboard views with real-time data visualization and intuitive user interface design.", color=TEXT_GREY, size=13),
                                ft.Text("• Data visualization with React Native", size=12, color=TEXT_GREY),
                                ft.Text("• Performance optimization", size=12, color=TEXT_GREY),
                            ])
                        ),
                        ft.Container(
                            col={"sm": 12, "md": 6},
                            bgcolor=BG_WHITE,
                            padding=20,
                            border_radius=8,
                            border=get_uniform_border(1, BORDER_COLOR),
                            content=ft.Column([
                                ft.Icon(ft.Icons.GRADIENT, color=PRIMARY_BLUE, size=28),
                                ft.Text("MATLAB & Mining Engineering", size=16, weight=ft.FontWeight.BOLD, color=DEEP_SLATE),
                                ft.Text("Completed multiple MATLAB certifications with 100% scores. Proficient in computational modeling for mining engineering applications.", color=TEXT_GREY, size=13),
                                ft.Text("• 7 MATLAB certifications completed", size=12, color=TEXT_GREY),
                                ft.Text("• Engineering computational modeling", size=12, color=TEXT_GREY),
                            ])
                        ),
                    ]
                )
            ]
        )
    )

    # 8. MATLAB Achievement Hub Section - Updated with correct image paths
    certificate_data = [
        {"title": "MATLAB Onramp", "image": IMAGES["matlab_onramp"]},
        {"title": "Simulink Onramp", "image": IMAGES["simulink_onramp"]},
        {"title": "Machine Learning Onramp", "image": IMAGES["machine_learning"]},
        {"title": "Reinforcement Learning Onramp", "image": IMAGES["reinforcement_learning"]},
        {"title": "Calculations with Vectors and Matrices", "image": IMAGES["calculations_vectors"]},
        {"title": "Explore Data with MATLAB Plots", "image": IMAGES["explore_data"]},
        {"title": "Make and Manipulate Matrices", "image": IMAGES["make_matrices"]},
    ]

    cert_cards = []
    for cert in certificate_data:
        img_control = ft.Image(
            src=cert["image"],
            height=150,
            fit="contain", 
            scale=1.0,
            animate_scale=ft.Animation(400, ft.AnimationCurve.EASE_OUT),
        )

        card_design = ft.Container(
            bgcolor=DARK_CARD_BG,
            padding=15,
            border_radius=10,
            border=get_uniform_border(1, ACCENT_TEAL),
            on_click=lambda e, title=cert["title"], img_src=cert["image"]: open_certificate_zoom(title, img_src),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        height=150,
                        width=320,
                        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                        border_radius=6,
                        bgcolor=BG_WHITE,
                        alignment=ft.Alignment(0, 0),
                        content=img_control,
                    ),
                    ft.Container(height=6),
                    ft.Text(cert["title"], weight=ft.FontWeight.BOLD, color=DARK_TEXT_WHITE, text_align=ft.TextAlign.CENTER, size=13, max_lines=2, overflow=ft.TextOverflow.ELLIPSIS),
                    ft.Text("Click to zoom", color=CERT_HINT, size=11, text_align=ft.TextAlign.CENTER),
                ],
            ),
        )

        hover_stack = ft.Stack(
            height=230,
            controls=[
                ft.Container(top=10, left=0, right=0, animate_position=ft.Animation(300, ft.AnimationCurve.EASE_OUT), content=card_design)
            ]
        )

        def make_hover_handler(stack_wrapper, target_img):
            inner_move_container = stack_wrapper.controls[0]
            def handle_hover(e):
                if e.data == "true":
                    inner_move_container.top = 0  
                    inner_move_container.shadow = ft.BoxShadow(blur_radius=12, color=ACCENT_TEAL)
                    target_img.scale = 1.05  
                else:
                    inner_move_container.top = 10  
                    inner_move_container.shadow = None
                    target_img.scale = 1.0
                inner_move_container.update()
                target_img.update()
            return handle_hover

        card_design.on_hover = make_hover_handler(hover_stack, img_control)
        cert_cards.append(ft.Container(col={"sm": 12, "md": 4}, content=hover_stack))

    certification_section = ft.Container(
        key="certificates",
        bgcolor=SECTION_DEEP,
        padding=40,
        content=ft.Column(
            spacing=20,
            controls=[
                create_section_header("MATLAB ACHIEVEMENT HUB", "Proof of completion for MATLAB and Simulink courses - All completed with 100%."),
                ft.Text("Click any certificate to zoom in and inspect the completion proof clearly.", size=13, color=SUBTEXT_GREY),
                ft.ResponsiveRow(spacing=20, run_spacing=10, controls=cert_cards),
            ],
        ),
    )

    # 9. GitHub Evidence & Documentation Section
    github_section = ft.Container(
        key="github",
        bgcolor=LIGHT_BG,
        padding=40,
        content=ft.Column(
            spacing=20,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Column([
                            ft.Text("GITHUB EVIDENCE & DOCUMENTATION", size=28, weight=ft.FontWeight.BOLD, color=PRIMARY_BLUE),
                            ft.Text("Verifiable individual contribution records for the MechTek project.", size=15, color=TEXT_GREY),
                        ]),
                        ft.IconButton(icon=ft.Icons.CODE, icon_color=PRIMARY_BLUE, tooltip="GitHub Evidence", url="https://github.com/mweutotalucky-prog")
                    ]
                ),
                ft.ResponsiveRow(
                    spacing=20,
                    run_spacing=20,
                    controls=[
                        ft.Container(
                            col={"sm": 12, "md": 4},
                            content=create_info_card(
                                "Commit History",
                                "Screenshots showing commits authored by Mweutota N Lukas for the MechTek mobile application development.",
                                ft.Icons.COMMIT,
                            ),
                        ),
                        ft.Container(
                            col={"sm": 12, "md": 4},
                            content=create_info_card(
                                "Pull Request Logs",
                                "Document code reviews performed, merge approvals, and repository management activities for the project team.",
                                ft.Icons.MERGE,
                            ),
                        ),
                        ft.Container(
                            col={"sm": 12, "md": 4},
                            content=create_info_card(
                                "Impact Summary",
                                "My UI/UX development and Firebase integration contributions ensured a fully functional fault reporting and maintenance tracking system.",
                                ft.Icons.INSIGHTS,
                            ),
                        ),
                    ],
                ),
                ft.ResponsiveRow(
                    spacing=20,
                    run_spacing=20,
                    controls=[
                        ft.Container(
                            col={"sm": 12, "md": 6},
                            bgcolor=BG_WHITE,
                            padding=20,
                            border_radius=10,
                            border=get_uniform_border(1, BORDER_COLOR),
                            content=ft.Column(
                                spacing=12,
                                controls=[
                                    ft.Row([ft.Icon(ft.Icons.CONSTRUCTION, color=PRIMARY_BLUE), ft.Text("MechTek-App", size=16, weight=ft.FontWeight.BOLD, color=DEEP_SLATE)]),
                                    ft.Text("Fault reporting and maintenance tracking mobile application built with React Native and Firebase for engineering teams.", size=13, color=TEXT_GREY),
                                    ft.Row(wrap=True, spacing=5, controls=[
                                        ft.Container(content=ft.Text("React Native", size=10, color=BG_WHITE), bgcolor=PRIMARY_BLUE, padding=4, border_radius=4),
                                        ft.Container(content=ft.Text("Firebase", size=10, color=BG_WHITE), bgcolor=ACCENT_TEAL, padding=4, border_radius=4),
                                        ft.Container(content=ft.Text("Fault Reporting", size=10, color=DEEP_SLATE), bgcolor=LIGHT_BG, padding=4, border_radius=4),
                                    ]),
                                    ft.Divider(color=BORDER_COLOR),
                                    ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                                        ft.Text("Active Development", size=11, color=SUBTEXT_GREY),
                                        ft.TextButton("View Repository", style=ft.ButtonStyle(color=ACCENT_TEAL), url="https://github.com/mweutotalucky-prog")
                                    ])
                                ]
                            )
                        ),
                        ft.Container(
                            col={"sm": 12, "md": 6},
                            bgcolor=BG_WHITE,
                            padding=20,
                            border_radius=10,
                            border=get_uniform_border(1, BORDER_COLOR),
                            content=ft.Column(
                                spacing=12,
                                controls=[
                                    ft.Row([ft.Icon(ft.Icons.DESCRIPTION, color=PRIMARY_BLUE), ft.Text("Project Documentation", size=16, weight=ft.FontWeight.BOLD, color=DEEP_SLATE)]),
                                    ft.Text("Comprehensive project documentation including requirements, design specifications, test plans, and deployment evidence.", size=13, color=TEXT_GREY),
                                    ft.Row(wrap=True, spacing=5, controls=[
                                        ft.Container(content=ft.Text("Documentation", size=10, color=BG_WHITE), bgcolor=PRIMARY_BLUE, padding=4, border_radius=4),
                                        ft.Container(content=ft.Text("Evidence", size=10, color=BG_WHITE), bgcolor=ACCENT_TEAL, padding=4, border_radius=4),
                                    ]),
                                    ft.Divider(color=BORDER_COLOR),
                                    ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                                        ft.Text("PDF Available", size=11, color=SUBTEXT_GREY),
                                        ft.TextButton("View Documentation", style=ft.ButtonStyle(color=ACCENT_TEAL))
                                    ])
                                ]
                            )
                        ),
                    ],
                ),
            ],
        ),
    )

    # 10. Advanced Contact Section
    name_field = ft.TextField(
        label="Your Full Name",
        border_color=PRIMARY_BLUE,
        focused_border_color=ACCENT_TEAL,
        text_style=ft.TextStyle(color=DEEP_SLATE)
    )
    email_field = ft.TextField(
        label="Email Address",
        border_color=PRIMARY_BLUE,
        focused_border_color=ACCENT_TEAL,
        text_style=ft.TextStyle(color=DEEP_SLATE)
    )
    subject_field = ft.Dropdown(
        label="Subject (Reason for Contact)",
        border_color=PRIMARY_BLUE,
        focused_border_color=ACCENT_TEAL,
        options=[
            ft.dropdown.Option("MechTek Project Inquiry"),
            ft.dropdown.Option("Mining Engineering Collaboration"),
            ft.dropdown.Option("Software Development Project"),
            ft.dropdown.Option("Internship/Job Opportunity"),
            ft.dropdown.Option("Technical Question"),
            ft.dropdown.Option("Other"),
        ],
        text_style=ft.TextStyle(color=DEEP_SLATE)
    )
    message_field = ft.TextField(
        label="Detailed Message",
        multiline=True,
        min_lines=5,
        max_lines=8,
        border_color=PRIMARY_BLUE,
        focused_border_color=ACCENT_TEAL,
        text_style=ft.TextStyle(color=DEEP_SLATE)
    )
    consent_checkbox = ft.Checkbox(
        label="I consent to having Mweutota N Lukas store my submitted information for the purpose of responding to my inquiry.",
        fill_color=PRIMARY_BLUE,
        check_color=BG_WHITE,
        value=False
    )

    def handle_submit_message(e):
        # Validation
        if not name_field.value or not email_field.value or not message_field.value or not subject_field.value:
            page.show_snack_bar(
                ft.SnackBar(
                    content=ft.Text("Please fill out all required fields (Name, Email, Subject, and Message)."),
                    bgcolor=ACCENT_TEAL,
                    action="Close",
                    action_color=BG_WHITE
                )
            )
        elif "@" not in email_field.value or "." not in email_field.value:
            page.show_snack_bar(
                ft.SnackBar(
                    content=ft.Text("Please enter a valid email address."),
                    bgcolor=ACCENT_TEAL,
                    action="Close",
                    action_color=BG_WHITE
                )
            )
        elif not consent_checkbox.value:
            page.show_snack_bar(
                ft.SnackBar(
                    content=ft.Text("Please consent to the data storage policy before submitting."),
                    bgcolor=ACCENT_TEAL,
                    action="Close",
                    action_color=BG_WHITE
                )
            )
        else:
            # Simulate sending message
            page.show_snack_bar(
                ft.SnackBar(
                    content=ft.Text(f"Thank you {name_field.value}! Your message regarding '{subject_field.value}' has been received. I'll respond to {email_field.value} soon."),
                    bgcolor=PRIMARY_BLUE,
                    action="Dismiss",
                    action_color=BG_WHITE,
                    duration=5000
                )
            )
            # Clear form after submission
            name_field.value = ""
            email_field.value = ""
            subject_field.value = None
            message_field.value = ""
            consent_checkbox.value = False
            page.update()

    def clear_form():
        name_field.value = ""
        email_field.value = ""
        subject_field.value = None
        message_field.value = ""
        consent_checkbox.value = False
        page.update()
        page.show_snack_bar(
            ft.SnackBar(
                content=ft.Text("Form cleared successfully."),
                bgcolor=PRIMARY_BLUE,
                action="Close",
                action_color=BG_WHITE
            )
        )

    contact_section = ft.Container(
        key="contact",
        bgcolor=BG_WHITE,
        padding=40,
        content=ft.Column([
            create_section_header("GET IN TOUCH", "Collaborate on mining engineering projects, MechTek development, or research opportunities."),
            ft.ResponsiveRow(
                spacing=30,
                controls=[
                    ft.Column(
                        col={"sm": 12, "md": 5},
                        spacing=20,
                        controls=[
                            ft.Text("Available for mining engineering consultations, software development collaborations, and research opportunities in mine safety and operational productivity.", color=TEXT_GREY, size=15),
                            ft.Divider(color=BORDER_COLOR),
                            ft.Text("📍 Namibia (UNAM Ongwediva Engineering Campus)", color=DEEP_SLATE, weight=ft.FontWeight.W_500, size=14),
                            ft.Text("✉️ lukasmweutota02@gmail.com", color=DEEP_SLATE, weight=ft.FontWeight.W_500, size=14),
                            ft.Text("📱 +264 81 784 8256", color=DEEP_SLATE, weight=ft.FontWeight.W_500, size=14),
                            ft.Text("🐙 mweutotalucky-prog", color=DEEP_SLATE, weight=ft.FontWeight.W_500, size=14),
                            ft.Text("⏱ Response time: 24-48 hours", color=TEXT_GREY, size=13),
                            ft.Card(
                                elevation=2,
                                content=ft.Container(
                                    bgcolor=SECTION_BLUE,
                                    padding=15,
                                    border_radius=8,
                                    content=ft.Column([
                                        ft.Text("Preferred Contact Methods:", weight=ft.FontWeight.BOLD, color=DEEP_SLATE),
                                        ft.Text("• Email for project proposals", size=13, color=TEXT_GREY),
                                        ft.Text("• LinkedIn for professional networking", size=13, color=TEXT_GREY),
                                        ft.Text("• Phone for urgent matters", size=13, color=TEXT_GREY),
                                    ])
                                )
                            )
                        ]
                    ),
                    ft.Container(
                        col={"sm": 12, "md": 7},
                        bgcolor=CARD_BG,
                        padding=30,
                        border_radius=12,
                        border=get_uniform_border(1, BORDER_COLOR),
                        content=ft.Column(
                            spacing=20,
                            controls=[
                                ft.Text("Send a Message About MechTek or Collaboration", size=18, weight=ft.FontWeight.BOLD, color=DEEP_SLATE),
                                name_field,
                                email_field,
                                subject_field,
                                message_field,
                                consent_checkbox,
                                ft.Divider(color=BORDER_COLOR),
                                ft.Row([
                                    ft.ElevatedButton(
                                        "Submit Message",
                                        icon=ft.Icons.SEND,
                                        bgcolor=PRIMARY_BLUE,
                                        color=BG_WHITE,
                                        on_click=handle_submit_message,
                                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=6))
                                    ),
                                    ft.TextButton(
                                        "Clear Form",
                                        on_click=lambda e: clear_form(),
                                        style=ft.ButtonStyle(color=ACCENT_TEAL)
                                    )
                                ], alignment=ft.MainAxisAlignment.END)
                            ]
                        )
                    )
                ]
            )
        ])
    )

    portfolio_pages = {
        "overview": hero_section,
        "skills": skills_section,
        "contribution": contribution_section,
        "timeline": timeline_section,
        "projects": project_section,
        "blog": blog_section,
        "experience": leadership_section,
        "certificates": certification_section,
        "github": github_section,
        "contact": contact_section,
    }

    page_switcher = ft.AnimatedSwitcher(
        content=build_page_view(hero_section, "overview"),
        duration=220,
        reverse_duration=160,
        switch_in_curve=ft.AnimationCurve.EASE_OUT,
        switch_out_curve=ft.AnimationCurve.EASE_IN,
        transition=ft.AnimatedSwitcherTransition.FADE,
        expand=True,
    )

    def make_nav_button(label, page_key):
        button = ft.TextButton(
            label,
            style=ft.ButtonStyle(
                color=BG_WHITE if page_key == current_page_key["value"] else NAV_INACTIVE,
                overlay_color=OVERLAY_TEAL,
            ),
            on_click=lambda e, target=page_key: navigate_to(target),
        )
        nav_buttons[page_key] = button
        return button

    # =========================================================
    # STICKY NAVBAR PANEL
    # =========================================================
    header_navbar = ft.Container(
        bgcolor=PRIMARY_BLUE,
        padding=ft.Padding(40, 15, 40, 15),
        border=ft.Border(bottom=ft.BorderSide(1, ACCENT_TEAL)),
        shadow=ft.BoxShadow(blur_radius=10, color=SHADOW_BLUE, offset=ft.Offset(0, 2)),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Row([
                    ft.Container(width=12, height=12, bgcolor=BG_WHITE, border_radius=6),
                    ft.Text("MWEUTOTA N LUKAS", weight=ft.FontWeight.BOLD, size=16, color=BG_WHITE, style=ft.TextStyle(letter_spacing=1.1))
                ], spacing=10),
                ft.Row([
                    make_nav_button("Overview", "overview"),
                    make_nav_button("Skills", "skills"),
                    make_nav_button("Portfolio", "contribution"),
                    make_nav_button("Timeline", "timeline"),
                    make_nav_button("Projects", "projects"),
                    make_nav_button("Blog", "blog"),
                    make_nav_button("Experience", "experience"),
                    make_nav_button("MATLAB Hub", "certificates"),
                    make_nav_button("GitHub", "github"),
                    make_nav_button("Contact", "contact"),
                ], spacing=10, wrap=True)
            ]
        )
    )

    # =========================================================
    # RENDER DIRECT TO MAIN PAGE WINDOW
    # =========================================================
    page.add(
        ft.Column(
            expand=True,
            spacing=0,
            controls=[
                header_navbar,
                page_switcher
            ]
        )
    )
if __name__ == "__main__":
    try:
        # Get port from environment variable or use default
        port = int(os.environ.get("PORT", 8551))
        
        # Run the Flet app in web mode
        ft.app(
            target=main,
            host="0.0.0.0",  # Bind to all interfaces
            port=port,
            assets_dir="assets",
            view=ft.AppView.WEB_BROWSER,  # This opens in web browser
            web_renderer=ft.WebRenderer.CANVAS_KIT,  # Use CanvasKit for better performance
        )
    except Exception as e:
        print(f"Error: {e}", flush=True)
        import traceback
        traceback.print_exc()