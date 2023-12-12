import dynamic from 'next/dynamic'

import {SunburstSvgProps } from '@nivo/sunburst'

import CenteredMetric from './CenteredMetric'


interface SunBurstFamilyProps {
        data: SunburstSvgProps<SunBurstFamilyData>["data"];
}

const ResponsiveSunburst = dynamic(()=>import('@nivo/sunburst').then((mod)=>mod.ResponsiveSunburst), {ssr: false})

const SunburstFamily = ({ data}: SunBurstFamilyProps) => (
    <ResponsiveSunburst
        data={data}
        margin={{ top: 10, right: 10, bottom: 10, left: 10 }}
        id="name"
        value="loc"
        valueFormat=" >-"
        cornerRadius={5}
        borderWidth={4}
        borderColor={{ theme: 'background' }}
        colors={{ scheme: 'nivo' }}
        childColor={{
            from: 'color',
            modifiers: [
                [
                    'brighter',
                    0.3
                ]
            ]
        }}
        enableArcLabels={true}
        arcLabel="value"
        arcLabelsSkipAngle={1}
        arcLabelsTextColor={{
            from: 'color',
            modifiers: [
                [
                    'darker',
                   10 
                ]
            ]
        }}
        layers={['arcs', 'arcLabels', CenteredMetric]}
    />

)

export default SunburstFamily;
