# from django import template
# 
# register = template.Library()
# 
# 
# @register.simple_tag
# def spinner_button(text="Run", button_class="btn-primary"):
#     return f"""
#     <button type="button" class="btn {button_class} disabled" data-toggle="tooltip" title="Running...">
#         <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
#         {text}
#     </button>
#     """
