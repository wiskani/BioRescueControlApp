export {}

declare global {
    interface SunBurstFamilyData {
        name: string
        color: string
        loc: number
        children: SunBurstFamilyData[]
    }

    interface BarChartFamilyData {
        family_name: string;
        rescue_count: number;
        rescue_color: string;
        relocation_count: number;
        relocation_color: string;
    }
    interface BarChartFamilyDataSpa {
        Familia: string;
        Rescates: number;
        color_rescate: string;
        Liberaciones: number;
        color_reubicacion: string;
    }
}
