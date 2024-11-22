def includeme(config):
    config.add_route("resume", "/resume")
    config.add_route("resume_pdf", "/resume/pdf")
    config.add_route("favicon", "/favicon.ico")
