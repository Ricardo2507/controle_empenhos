document.body.addEventListener('htmx:afterSwap', function (event) {
  if (event.detail.target.id === 'modalContent') {
    const modal = bootstrap.Modal.getOrCreateInstance(document.getElementById('modalGlobal'));
    modal.show();
  }
});

document.body.addEventListener('htmx:beforeSwap', function (event) {
  if (event.detail.xhr.status === 204) {
    event.detail.shouldSwap = false;
  }
});

$(function () {
  $('.datatable').DataTable({
    language: { url: 'https://cdn.datatables.net/plug-ins/1.13.8/i18n/pt-BR.json' },
    pageLength: 25,
    responsive: true,
    dom: '<"d-flex justify-content-between align-items-center mb-3"Bf>rt<"d-flex justify-content-between align-items-center mt-3"ip>',
    buttons: [
      { extend: 'copy', text: 'Copiar' },
      { extend: 'excel', text: 'Excel' },
      { extend: 'pdf', text: 'PDF' },
      { extend: 'print', text: 'Imprimir' }
    ]
  });
});
