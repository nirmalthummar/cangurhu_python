from rest_framework.renderers import JSONRenderer


class CustomRenderer(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context['response'].status_code
        response = {
          "status": "success",
          "code": status_code,
          "data": data,
          "message": "ok"
        }

        if not str(status_code).startswith('2'):
            response["status"] = "error"
            response["data"] = {}
            try:
                response["message"] = data["detail"]
            except KeyError:
                for k, v in data.items():
                    response["message"] = f"{k}: {v}"
                    break

        return super(CustomRenderer, self).render(response, accepted_media_type, renderer_context)

