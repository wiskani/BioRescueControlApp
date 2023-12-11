interface CenteredMetricProps {
        dataWithArc: SunBurstFamilyData;
        centerX: number;
        centerY: number;
        }
function sumLoc(data: SunBurstFamilyData): number {
    // Sumar el valor de loc del nivel actual
    let total = data.loc;

    // Si hay hijos, sumar recursivamente sus valores de loc
    if (data.children && data.children.length > 0) {
        data.children.forEach(child => {
            total += sumLoc(child);
        });
    }

    return total;
}

const CenteredMetric: React.FC<CenteredMetricProps> = ({ dataWithArc, centerX, centerY }) => {
        const totalLoc = sumLoc(dataWithArc);

        return (
            <text
                x={centerX}
                y={centerY}
                textAnchor="middle"
                dominantBaseline="central"
                fill='white'
                style={{
                    fontSize: '42px',
                    fontWeight: 600,
                }}
            >
                {totalLoc}
            </text>
        )
    }

export default CenteredMetric;
