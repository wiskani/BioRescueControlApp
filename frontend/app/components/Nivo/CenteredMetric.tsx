import { SunburstCustomLayerProps} from "@nivo/sunburst";
type RawDatum = SunBurstFamilyData;
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

const CenteredMetric: React.FC<SunburstCustomLayerProps<any>> = ({ nodes, centerX, centerY }) => {
        const totalLoc = nodes.reduce((acc, node) => acc + node.value, 0);

        return (
        <>
            <text
                x={centerX}
                y={centerY}
                textAnchor="middle"
                dominantBaseline="central"
                fill='black'
                style={{
                    fontSize: '42px',
                    fontWeight: 600,
                }}
            >
                {totalLoc/2}
            </text>
            <text
                fill='black'
                x={centerX}
                y={centerY+50}
                textAnchor="middle"
                dominantBaseline="central"
                style={{
                    fontSize: '15px',
                    fontWeight: 600,
                }}

            >
            Especimenes rescatados
            </text>
            </>
        )
    }

export default CenteredMetric;
