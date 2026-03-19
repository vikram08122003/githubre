(function () {
  const grid = document.getElementById('newsGrid');
  if (!grid) return;

  fetch('/news/' + symbol)
    .then(function(r) { return r.json(); })
    .then(function(articles) {

      if (!articles || articles.length === 0) {
        grid.innerHTML = '<p class="text-muted">No news found.</p>';
        return;
      }

      var html = '';
      for (var i = 0; i < articles.length; i++) {
        var item = articles[i];
        var title  = item.title  ? item.title.replace(/ - .*$/, '')  : 'No title';
        var source = item.source ? item.source : 'News';
        var pub    = item.published ? item.published.substring(0, 16) : '';
        var link   = item.link ? item.link : '#';

        html += '<a class="news-card" href="' + link + '" target="_blank" rel="noopener">';
        html += '<div class="news-source">' + source + '</div>';
        html += '<div class="news-title">'  + title  + '</div>';
        html += '<div class="news-time">'   + pub    + '</div>';
        html += '</a>';
      }

      grid.innerHTML = html;
    })
    .catch(function(err) {
      console.error('News error:', err);
      grid.innerHTML = '<p class="text-muted">Could not load news.</p>';
    });

})();