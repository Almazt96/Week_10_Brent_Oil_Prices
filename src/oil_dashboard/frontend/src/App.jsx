import React, { useState, useEffect } from 'react';
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ReferenceDot } from 'recharts';
import { Calendar, AlertCircle, TrendingUp, ShieldAlert } from 'lucide-react';

function App() {
  const [priceData, setPriceData] = useState([]);
  const [events, setEvents] = useState([]);
  const [selectedEvent, setSelectedEvent] = useState(null);
  const [startDate, setStartDate] = useState('2024-01-01');
  const [endDate, setEndDate] = useState('2024-01-05');
  const [loading, setLoading] = useState(true);

  // Fetch Data from Flask Backend
  useEffect(() => {
    setLoading(true);
    Promise.all([
      fetch(`http://127.0.0.1:5000/api/historical-prices?start_date=${startDate}&end_date=${endDate}`).then(res => res.json()),
      fetch('http://127.0.0.1:5000/api/event-correlations').then(res => res.json())
    ])
    .then(([pricesRes, eventsRes]) => {
      setPriceData(pricesRes.data);
      setEvents(eventsRes.data);
      setLoading(false)
    })
    .catch(err => {
      console.error("Error fetching dashboard data:", err);
      setLoading(false);
    });
  }, [startDate, endDate]);

  // Highlight an event when clicked
  const handleEventClick = (event) => {
    setSelectedEvent(event);
  };

  return (
    <div style={{ backgroundColor: '#f3f4f6', minHeight: '100vh', padding: '24px', fontFamily: 'sans-serif' }}>
      
      {/* Header */}
      <header style={{ marginBottom: '24px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '16px' }}>
        <div>
          <h1 style={{ fontSize: '28px', fontWeight: 'bold', color: '#1f2937', margin: 0 }}>Brent Crude Oil Analysis Dashboard</h1>
          <p style={{ color: '#6b7280', margin: '4px 0 0 0' }}>Investigating geopolitical & economic event impacts on global energy markets</p>
        </div>
        
        {/* Filters */}
        <div style={{ display: 'flex', gap: '12px', backgroundColor: '#fff', padding: '12px', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
            <Calendar size={18} color="#4b5563" />
            <input type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} style={{ border: '1px solid #d1d5db', borderRadius: '4px', padding: '4px' }} />
          </div>
          <span style={{ alignSelf: 'center' }}>to</span>
          <input type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)} style={{ border: '1px solid #d1d5db', borderRadius: '4px', padding: '4px' }} />
        </div>
      </header>

      {loading ? (
        <div style={{ textAlign: 'center', padding: '48px', fontSize: '18px' }}>Loading analysis models...</div>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: '1fr', gap: '24px' }}>
          
          {/* Main Chart Section */}
          <div style={{ backgroundColor: '#fff', padding: '24px', borderRadius: '12px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
            <h2 style={{ fontSize: '18px', fontWeight: '600', marginBottom: '16px' }}>Price Trends & Event Detection Marker</h2>
            <div style={{ width: '100%', height: 350 }}>
              <ResponsiveContainer>
                <LineChart data={priceData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                  <XAxis dataKey="date" stroke="#9ca3af" />
                  <YAxis stroke="#9ca3af" domain={['auto', 'auto']} label={{ value: 'Price (USD/bbl)', angle: -90, position: 'insideLeft', offset: 10 }} />
                  <Tooltip />
                  <Line type="monotone" dataKey="price" stroke="#2563eb" strokeWidth={3} dot={{ r: 4 }} activeDot={{ r: 8 }} />
                  
                  {/* Highlight specific event point dynamically if selected */}
                  {events.map((ev, idx) => (
                    <ReferenceDot 
                      key={idx}
                      x={ev.date} 
                      y={priceData.find(p => p.date === ev.date)?.price || 80} 
                      r={8} 
                      fill={selectedEvent?.id === ev.id ? "#dc2626" : "#f59e0b"} 
                      stroke="#fff"
                      strokeWidth={2}
                    />
                  ))}
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Interactive Drill-down Split Grid */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '24px' }}>
            
            {/* Impacting Events List */}
            <div style={{ backgroundColor: '#fff', padding: '20px', borderRadius: '12px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
              <h3 style={{ fontSize: '16px', fontWeight: '600', marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                <ShieldAlert color="#f59e0b" /> Tracked Geopolitical Events
              </h3>
              <div style={{ display: 'flex', flexStack: 'column', gap: '10px' }}>
                {events.map((ev) => (
                  <div 
                    key={ev.id} 
                    onClick={() => handleEventClick(ev)}
                    style={{ 
                      padding: '12px', 
                      borderRadius: '8px', 
                      border: `2px solid ${selectedEvent?.id === ev.id ? '#2563eb' : '#e5e7eb'}`, 
                      cursor: 'pointer',
                      transition: '0.2s',
                      backgroundColor: selectedEvent?.id === ev.id ? '#eff6ff' : '#fff'
                    }}
                  >
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
                      <span style={{ fontSize: '12px', fontWeight: 'bold', color: '#6b7280' }}>{ev.date}</span>
                      <span style={{ fontSize: '12px', color: '#dc2626', fontWeight: '600' }}>{ev.price_impact_3d} Impact</span>
                    </div>
                    <div style={{ fontWeight: '500', color: '#1f2937' }}>{ev.event}</div>
                  </div>
                ))}
              </div>
            </div>

            {/* Drill-Down Details Panel */}
            <div style={{ backgroundColor: '#fff', padding: '20px', borderRadius: '12px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
              <h3 style={{ fontSize: '16px', fontWeight: '600', marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                <TrendingUp color="#2563eb" /> Correlation Drill-down Insights
              </h3>
              {selectedEvent ? (
                <div>
                  <h4 style={{ margin: '0 0 8px 0', color: '#1f2937', fontSize: '18px' }}>{selectedEvent.event}</h4>
                  <p style={{ fontSize: '14px', color: '#4b5563', lineHeight: '1.5' }}>{selectedEvent.description}</p>
                  
                  <div style={{ marginTop: '16px', padding: '12px', backgroundColor: '#f9fafb', borderRadius: '6px', display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
                    <div>
                      <div style={{ fontSize: '12px', color: '#6b7280' }}>Category</div>
                      <div style={{ fontWeight: '600', color: '#374151' }}>{selectedEvent.category}</div>
                    </div>
                    <div>
                      <div style={{ fontSize: '12px', color: '#6b7280' }}>Quantified Shock</div>
                      <div style={{ fontWeight: '600', color: '#dc2626' }}>{selectedEvent.price_impact_3d} (3-day window)</div>
                    </div>
                  </div>
                </div>
              ) : (
                <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '150px', color: '#9ca3af' }}>
                  <AlertCircle size={32} style={{ marginBottom: '8px' }} />
                  <p style={{ margin: 0, fontSize: '14px' }}>Click an event on the left to unpack stakeholders metrics.</p>
                </div>
              )}
            </div>

          </div>
        </div>
      )}
    </div>
  );
}

export default App;