import dynamic from 'next/dynamic'

import { BarSvgProps } from '@nivo/bar';

interface BarChartFamilyDataFlex extends BarChartFamilyData {
    [key: string]: string | number;
}


interface BarChartFamilyProps {
        data: BarSvgProps<BarChartFamilyDataFlex>["data"];
}

const ResponsiveBar = dynamic(
    ()=>import('@nivo/bar').then((mod)=>mod.ResponsiveBar), {ssr: false}
)

const BarChartFamily = ({ data}: BarChartFamilyProps) => (
    <ResponsiveBar
        data={data}
        keys={data.map((d)=>d.family_name)}
        indexBy={"family_name"}
        margin={{ top: 10, right: 10, bottom: 10, left: 10 }}
        padding={0.3}
        valueScale={{ type: 'linear' }}
        indexScale={{ type: 'band', round: true }}
        colors={{ scheme: 'nivo' }}

    />

)

export default BarChartFamily;
