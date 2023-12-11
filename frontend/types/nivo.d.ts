export {}

declare global {
        interface SunBurstFamilyData {
                name: string
                color: string
                loc: number
                children: SunBurstFamilyData[]
        }
}

