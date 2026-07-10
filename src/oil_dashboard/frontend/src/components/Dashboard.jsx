import React, { useState, useEffect } from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceDot } from 'recharts';
import { Calendar, DollarSign, AlertTriangle, TrendingUp, Filter } from 'lucide-react';
import MetricCard from './MetricCard';

export default function Dashboard() {
  const [data, setData] = useState([]);
  const [metrics, setMetrics] = useState(null);
  const [selectedEvent, setSelectedEvent] = useState(null);
  const [startDate, setStartDate] = useState('2020-01-01');
  const [endDate, setEndDate] = useState('2026-12-31');
  const [categoryFilter, setCategoryFilter] = useState('All');

  useEffect(() => {
    // Fetch metrics
    fetch('http://localhost:5000/api/metrics')
      .then(res => res.json())
      .then(data => setMetrics(data));
  }, []);

  useEffect(() => {
    // Fetch time-series historical data with filters
    fetch(`http://localhost:5000/api/historical?start_date=${startDate}&end_date=${endDate}`)
      .then(res => res.json())
      .then(data => setData(data));
  }, [startDate, endDate]);

  // Client-side filtering logic for explicit categorical events
  const filteredData = data.filter(item => {
    if (categoryFilter === 'All') return true;
    return item.category === categoryFilter || !item.event; 
  });

  const eventsList = data.filter(item => item.event && (categoryFilter === 'All' || item.category === categoryFilter));

  return (
    <div className="min-h-screen bg-gray-50 p-4 md:p-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Brent Crude Oil Price Analytics</h1>
        <p className="text-gray-500 mt-1">Explore the impact of geopolitical and macroeconomic events on global energy markets.</p>
      </div>

      {/* Metric KPI Grid */}
      {metrics && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          <MetricCard title="Avg Price (Period)" value={`$${metrics.average_price}`} icon={<DollarSign size={20} />} subtitle="USD per Barrel" />
          <MetricCard title="Peak Price" value={`$${metrics.peak_price}`} icon={<TrendingUp size={20} />} subtitle="Max structural point" />
          <MetricCard title="Avg Event Volatility" value={`${metrics.avg_event_volatility}%`} icon={<AlertTriangle size={20} />} subtitle="Fluctuation intensity" />
          <MetricCard title="Tracked Key Events" value={metrics.total_tracked_events} icon={<Calendar size={20} />} subtitle="Major global disruptions" />
        </div>
      )}

      {/* Control Configuration Panel */}
      <div className="bg-white p-4 rounded-xl shadow-sm border border-gray-100 mb-8 grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Start Date</label>
          <input type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} className="w-full border rounded-lg p-2 text-sm focus:ring-2 focus:ring-blue-500 outline-none" />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">End Date</label>
          <input type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)} className="w-full border rounded-lg p-2 text-sm focus:ring-2 focus:ring-blue-500 outline-none" />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Event Category</label>
          <select value={categoryFilter} onChange={(e) => setCategoryFilter(e.target.value)} className="w-full border rounded-lg p-2 text-sm focus:ring-2 focus:ring-blue-500 outline-none">
            <option value="All">All Categories</option>
            <option value="Conflict">Conflicts / Wars</option>
            <option value="Political Decision">Political Decisions</option>
            <option value="Economic Sanction/Shock">Economic Sanctions & Shocks</option>
          </select>
        </div>
      </div>

      {/* Chart Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 lg:col-span-2">
          <h2 className="text-xl font-semibold mb-4 text-gray-800">Price Trend & Highlighted Structural Shifts</h2>
          <div className="h-80 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={filteredData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorPrice" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.2}/>
                    <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f3f4f6" />
                <XAxis dataKey="date" tick={{fontSize: 12}} stroke="#9ca3af" />
                <YAxis domain={['auto', 'auto']} tick={{fontSize: 12}} stroke="#9ca3af" tickFormatter={(v) => `$${v}`} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#fff', border: '1px solid #e5e7eb', borderRadius: '8px' }}
                  formatter={(value, name, props) => [`$${value}`, props.payload.event ? `Event: ${props.payload.event}` : 'Standard Trading']}
                />
                <Area type="monotone" dataKey="price" stroke="#3b82f6" strokeWidth={2} fillOpacity={1} fill="url(#colorPrice)" />
                
                {/* Dynamically emphasize the event selected in the side panel */}
                {selectedEvent && (
                  <ReferenceDot x={selectedEvent.date} y={selectedEvent.price} r={8} fill="#ef4444" stroke="#fff" strokeWidth={2} />
                )}
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Drill-Down Sidebar (Interactivity Anchor) */}
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex flex-col max-h-[460px]">
          <h2 className="text-xl font-semibold mb-2 text-gray-800">Event Explorer</h2>
          <p className="text-xs text-gray-400 mb-4">Click any event below to pinpoint it on the main macro timeline.</p>
          <div className="overflow-y-auto space-y-3 flex-1 pr-1">
            {eventsList.map((ev, idx) => (
              <div 
                key={idx} 
                onClick={() => setSelectedEvent(ev)}
                className={`p-3 rounded-lg border text-left cursor-pointer transition-all ${
                  selectedEvent?.date === ev.date 
                    ? 'border-blue-500 bg-blue-50/50 shadow-sm' 
                    : 'border-gray-100 hover:bg-gray-50'
                }`}
              >
                <div className="flex justify-between items-start">
                  <span className="text-xs font-semibold text-blue-600 bg-blue-50 px-2 py-0.5 rounded-full">{ev.category}</span>
                  <span className="text-xs text-gray-400 font-mono">{ev.date}</span>
                </div>
                <p className="text-sm font-medium text-gray-800 mt-2">{ev.event}</p>
                <div className="mt-2 pt-2 border-t border-dashed border-gray-100 flex justify-between text-xs text-gray-500">
                  <span>Price: <strong className="text-gray-700">${ev.price}</strong></span>
                  <span>Volatility Index: <strong className="text-gray-700">{ev.volatility}%</strong></span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}