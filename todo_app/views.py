from typing import Any, Dict
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from todo_app.models import ToDoItem, ToDoList

class ListsListView(ListView):
    """List View for the to-do lists themselves"""
    model = ToDoList
    template_name = 'todo_app/index.html'

class ItemsListView(ListView):
    """List View for the items in a single to-do list"""
    model = ToDoItem
    template_name = 'todo_app/todo_list.html'

    def get_queryset(self) -> 'QuerySet[T]':
        return ToDoItem.objects.filter(todo_list_id=self.kwargs['list_id'])
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['todo_list'] = ToDoList.objects.get(id=self.kwargs['list_id'])
        return context

class ListCreate(CreateView):
    model = ToDoList
    fields = ['title']

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(ListCreate, self).get_context_data(**kwargs)
        context['title'] = 'Add a new list'
        return context

class ItemCreate(CreateView):
    model = ToDoItem
    fields = ['todo_list', 'title', 'description', 'due_date']

    def get_initial(self) -> Dict[str, Any]:
        initial_data = super(ItemCreate, self).get_initial()
        todo_list = ToDoList.objects.get(id=self.kwargs['list_id'])
        initial_data['todo_list'] = todo_list
        return initial_data

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(ItemCreate, self).get_context_data(**kwargs)
        todo_list = ToDoList.objects.get(id=self.kwargs['list_id'])
        context['todo_list'] = todo_list
        context['title'] = 'Create a new item'
        return context

    def get_success_url(self) -> str:
        return reverse('list', args=[self.object.todo_list_id])

class ItemUpdate(UpdateView):
    model = ToDoItem
    fields = ['todo_list', 'title', 'description', 'due_date']

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(ItemUpdate, self).get_context_data(**kwargs)
        todo_list = ToDoList.objects.get(id=self.kwargs['list_id'])
        context['todo_list'] = todo_list
        context['title'] = 'Edit item'
        return context

    def get_success_url(self) -> str:
        return reverse('list', args=[self.object.todo_list_id])

class ListDelete(DeleteView):
    model = ToDoList
    sucess_url = reverse_lazy('index')

class ItemDelete(DeleteView):
    model = ToDoItem

    def get_success_url(self) -> str:
        return reverse_lazy('list', args=[self.kwargs['list_id']])

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['todo_list'] = self.object.todo_list
        return context