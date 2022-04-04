from typing import Any, Dict
from django.views.generic import ListView
from todo_app.models import ToDoItem, ToDoList

class ListListView(ListView):
    """List View for the to-do lists themselves"""
    model = ToDoList
    template_name = 'todo_app/index.html'

class ItemListView(ListView):
    model = ToDoItem
    template_name = 'todo_app/todo_list.html'

    def get_queryset(self) -> 'QuerySet[T]':
        return ToDoItem.objects.filter(todo_list_id=self.kwargs['list_id'])
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['todo_list'] = ToDoList.objects.get(id=self.kwargs['list_id'])
        return context