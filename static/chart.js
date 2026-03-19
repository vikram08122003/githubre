new Chart(document.getElementById('priceChart'), {
  type: 'line',
  data: {
    labels: dates,
    datasets: [{
      label: symbol + ' Price',
      data: prices,
      borderColor: '#00e5ff',
      backgroundColor: 'rgba(0,229,255,0.06)',
      fill: true, tension: 0.3, pointRadius: 0, borderWidth: 2,
    }]
  },
  options: {
    responsive: true, maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
      tooltip: {
        mode: 'index', intersect: false,
        callbacks: { label: ctx => ' ₹' + ctx.raw.toLocaleString('en-IN', { minimumFractionDigits: 2 }) }
      }
    },
    scales: {
      x: { ticks: { color: '#5a6a80', font: { size: 10 }, maxTicksLimit: 8 }, grid: { color: 'rgba(255,255,255,0.04)' } },
      y: { ticks: { color: '#5a6a80', font: { size: 10 }, callback: v => '₹' + v.toLocaleString('en-IN') }, grid: { color: 'rgba(255,255,255,0.04)' } }
    }
  }
});

new Chart(document.getElementById('rsiChart'), {
  type: 'line',
  data: {
    labels: dates,
    datasets: [
      { label: 'RSI', data: rsi, borderColor: '#ff4d6d', backgroundColor: 'rgba(255,77,109,0.06)', fill: true, tension: 0.3, pointRadius: 0, borderWidth: 2 },
      { label: 'Overbought 70', data: Array(dates.length).fill(70), borderColor: 'rgba(255,183,0,0.4)', borderDash: [4,4], pointRadius: 0, borderWidth: 1, fill: false },
      { label: 'Oversold 30',   data: Array(dates.length).fill(30), borderColor: 'rgba(0,214,143,0.4)', borderDash: [4,4], pointRadius: 0, borderWidth: 1, fill: false }
    ]
  },
  options: {
    responsive: true, maintainAspectRatio: false,
    plugins: { legend: { display: false }, tooltip: { mode: 'index', intersect: false } },
    scales: {
      x: { ticks: { color: '#5a6a80', font: { size: 10 }, maxTicksLimit: 8 }, grid: { color: 'rgba(255,255,255,0.04)' } },
      y: { min: 0, max: 100, ticks: { color: '#5a6a80', font: { size: 10 } }, grid: { color: 'rgba(255,255,255,0.04)' } }
    }
  }
});