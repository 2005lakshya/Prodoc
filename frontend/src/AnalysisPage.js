import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import LoadingScreen from './loading_screen/LoadingScreen';

function AnalysisPage() {
    const location = useLocation();
    const navigate = useNavigate();
    const { file } = location.state || {};
    const [loading, setLoading] = useState(true);
    const [analysisResult, setAnalysisResult] = useState(null);
    const [error, setError] = useState(null);


    useEffect(() => {
        if (file) {
            const formData = new FormData();
            formData.append('file', file);

            fetch('http://localhost:8001/upload', {
                method: 'POST',
                body: formData,
            })
                .then(res => {
                    if (!res.ok) throw new Error('Server error');
                    return res.json();
                })
                .then(data => {
                    if (data.error) {
                        setError(data.error);
                        setLoading(false);
                        return;
                    }
                    setAnalysisResult(data);
                    setLoading(false);
                })
                .catch(err => {
                    console.error('Analysis failed:', err);
                    setError('Backend not working. Please check if the server is running on port 8001.');
                    setLoading(false);
                });
        } else {
            setLoading(false);
        }
    }, [file]);

    if (loading) {
        return <LoadingScreen />;
    }

    if (!file) {
        return (
            <div style={{
                backgroundColor: 'transparent',
                minHeight: '100vh',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                color: 'white'
            }}>
                <h2>No file found for analysis.</h2>
                <button onClick={() => navigate('/')} style={{
                    padding: '10px 20px',
                    background: '#4CAF50',
                    border: 'none',
                    borderRadius: '5px',
                    color: 'white',
                    cursor: 'pointer',
                    marginTop: '20px'
                }}>
                    Go Back
                </button>
            </div>
        );
    }

    const result = analysisResult;

    return (
        <div style={{
            backgroundColor: 'transparent',
            minHeight: '100vh',
            width: '100%',
            color: 'white',
            display: 'flex',
            flexDirection: 'column',
            padding: '20px',
            boxSizing: 'border-box',
            overflow: 'hidden'
        }}>
            {/* Header */}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
                    <img src="/logo.png" alt="Logo" style={{ width: '50px' }} />
                    <h1 style={{ fontSize: '1.5rem', margin: 0, fontWeight: 'bold' }}>PRO DOC</h1>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
                    {error && (
                        <span style={{ fontSize: '0.8rem', color: '#ff5252', background: 'rgba(0,0,0,0.3)', padding: '5px 15px', borderRadius: '15px' }}>
                            {error}
                        </span>
                    )}
                    <button
                        onClick={() => navigate('/')}
                        style={{
                            padding: '8px 20px',
                            background: 'rgba(255, 255, 255, 0.1)',
                            border: '1px solid rgba(255, 255, 255, 0.3)',
                            borderRadius: '20px',
                            color: 'white',
                            cursor: 'pointer',
                        }}
                    >
                        Back to Home
                    </button>
                </div>
            </div>

            <div style={{ display: 'flex', flex: 1, gap: '20px', overflow: 'hidden' }}>
                {/* Left Side: Flagged Highlights */}
                <div style={{
                    flex: 1,
                    backgroundColor: 'rgba(0,0,0,0.3)',
                    borderRadius: '20px',
                    backdropFilter: 'blur(10px)',
                    border: '1px solid rgba(255,255,255,0.1)',
                    display: 'flex',
                    flexDirection: 'column',
                    overflow: 'hidden'
                }}>
                    <div style={{ padding: '15px', borderBottom: '1px solid rgba(255,255,255,0.1)', background: 'rgba(255,255,255,0.05)' }}>
                        <h3 style={{ margin: 0, fontSize: '1rem', color: '#ff5252' }}>Risk Highlights</h3>
                    </div>
                    <div style={{ flex: 1, padding: '20px', overflowY: 'auto' }}>
                        {result?.highlights?.map((h, idx) => (
                            <div key={idx} style={{ marginBottom: '20px', padding: '15px', background: 'rgba(255,255,255,0.02)', borderRadius: '10px', borderLeft: '3px solid #ff5252' }}>
                                <div style={{ fontWeight: 'bold', color: '#ff5252', marginBottom: '5px', fontSize: '0.9rem' }}>{h.label}</div>
                                <div style={{ fontSize: '0.9rem', opacity: 0.8, lineHeight: '1.5' }}>{h.text}</div>
                            </div>
                        ))}
                        {(!result?.highlights || result.highlights.length === 0) && (
                            <div style={{ opacity: 0.5, textAlign: 'center', marginTop: '40px' }}>No risks detected on the left.</div>
                        )}
                    </div>
                </div>

                {/* Right Side: Backend Results */}
                <div style={{
                    flex: 1,
                    backgroundColor: 'rgba(255,255,255,0.05)',
                    borderRadius: '20px',
                    backdropFilter: 'blur(15px)',
                    border: '1px solid rgba(255,255,255,0.1)',
                    display: 'flex',
                    flexDirection: 'column',
                    overflow: 'hidden'
                }}>
                    <div style={{ padding: '15px', borderBottom: '1px solid rgba(255,255,255,0.1)', background: 'rgba(255,255,255,0.07)' }}>
                        <h3 style={{ margin: 0, fontSize: '1rem', color: '#69f0ae' }}>Analysis Backend Results</h3>
                    </div>

                    <div style={{ flex: 1, padding: '25px', overflowY: 'auto' }}>
                        {result && (
                            <div style={{ display: 'flex', flexDirection: 'column', gap: '25px' }}>
                                <div>
                                    <div style={{ fontSize: '0.8rem', opacity: 0.6, marginBottom: '5px' }}>RISK SCORE</div>
                                    <div style={{ fontSize: '3rem', fontWeight: 'bold', color: '#ffd740' }}>{result.risk_score}</div>
                                </div>

                                <div>
                                    <div style={{ fontSize: '0.8rem', opacity: 0.6, marginBottom: '5px' }}>DECISION</div>
                                    <div style={{ fontSize: '1.2rem', fontWeight: 'bold' }}>{result.decision}</div>
                                </div>

                                <div>
                                    <div style={{ fontSize: '0.8rem', opacity: 0.6, marginBottom: '5px' }}>JUSTIFICATION REPORT</div>
                                    <div style={{ fontSize: '0.95rem', opacity: 0.9, lineHeight: '1.6', whiteSpace: 'pre-wrap' }}>
                                        {result.justification_report}
                                    </div>
                                </div>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}

export default AnalysisPage;
