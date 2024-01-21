from resource_management.views.Constants import MEDIA_UPLOADS__HTML_KEY, MEDIA_UPLOADS_NOTE__HTML_KEY, \
    MEDIA_UPLOADS_EVENT_TYPE__HTML_KEY, MEDIA_UPLOADS_EVENT_DATE__HTML_KEY, MEDIA_UPLOADS__HTML_NAME, \
    MEDIA_UPLOADS_NOTE__HTML_NAME, MEDIA_UPLOADS_EVENT_TYPE__HTML_NAME, MEDIA_UPLOADS_EVENT_DATE__HTML_NAME, \
    MEDIA_UPLOADS_EVENT_TYPE_SPECIFIER__HTML_KEY, MEDIA_UPLOADS_EVENT_TYPE_SPECIFIER__HTML_NAME


def create_context_for_upload_media_html(context):
    context.update({
        MEDIA_UPLOADS__HTML_KEY: MEDIA_UPLOADS__HTML_NAME,
        MEDIA_UPLOADS_NOTE__HTML_KEY: MEDIA_UPLOADS_NOTE__HTML_NAME,
        MEDIA_UPLOADS_EVENT_TYPE__HTML_KEY: MEDIA_UPLOADS_EVENT_TYPE__HTML_NAME,
        MEDIA_UPLOADS_EVENT_DATE__HTML_KEY: MEDIA_UPLOADS_EVENT_DATE__HTML_NAME,
        MEDIA_UPLOADS_EVENT_TYPE_SPECIFIER__HTML_KEY: MEDIA_UPLOADS_EVENT_TYPE_SPECIFIER__HTML_NAME
    })