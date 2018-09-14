from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

def index(request):
	return render(request, 'app/index.html')

def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None

class pdf(View):
	def get(self, request, *args, **kwargs):
		template = get_template('app/pdf.html')
		context = {
			"invoice_id": 123,
			"customer_name": "John Cooper",
			"amount": 1399.99,
			"today": "Today",
			}
		html = template.render(context)
		pdf = render_to_pdf('app/pdf.html', context)
		if pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			filename = "Invoice_%s.pdf" %("12341231")
			content = "inline; filename='%s'" %(filename)
			download = request.GET.get("download")
			if download:
				content = "attachment; filename='%s'" %(filename)
			response['Content-Disposition'] = content
			return response
		return HttpResponse("Not found")