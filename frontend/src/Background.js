import React from 'react';
import LiquidEther from './LiquidEther/LiquidEther';

const Background = ({ children }) => {
    return (
        <div style={{ position: 'relative', minHeight: '100vh', width: '100%', overflow: 'hidden' }}>
            <div style={{
                position: 'fixed',
                top: 0,
                left: 0,
                width: '100%',
                height: '100%',
                zIndex: -1,
                backgroundColor: '#0a0a0a' // Fallback color
            }}>
                <LiquidEther
                    colors={['#5227FF', '#FF9FFC', '#B19EEF']}
                    mouseForce={20}
                    cursorSize={100}
                    isViscous
                    viscous={30}
                    iterationsViscous={32}
                    iterationsPoisson={32}
                    resolution={0.5}
                    isBounce={false}
                    autoDemo
                    autoSpeed={0.5}
                    autoIntensity={2.2}
                    takeoverDuration={0.25}
                    autoResumeDelay={3000}
                    autoRampDuration={0.6}
                    // The user provided color0, color1, color2 props which aren't in the default LiquidEther props but I'll pass them in case their customized version uses them
                    color0="#5d323f"
                    color1="#FF9FFC"
                    color2="#B19EEF"
                />
            </div>
            <div style={{ position: 'relative', zIndex: 1 }}>
                {children}
            </div>
        </div>
    );
};

export default Background;
