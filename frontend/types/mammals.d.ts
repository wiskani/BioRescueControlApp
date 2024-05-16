export {}

declare global {
    interface RescueMammalsWithSpecieData {
        cod: string; 
        date: Date; 
        longitude: number; 
        latitude: number ;
        observation: string|null; 
        specie_name: string | null; 
        genus_name: string | null; 
    }

    interface ReleaseMammalsWithSpecieData {
        cod: string;
        longitude: number | null;
        latitude: number | null;
        altitude: number | null;
        sustrate: string | null;
        site_release_mammals: string;
        specie_name: string | null;
        genus_name: string | null;
    }

    interface RescueMammalsWithSpecieExtendedData extends RescueMammalsWithSpecieData {
        mark: string;
        gender: stringing | null;
        LT: number | null;
        LC: number | null;
        LP: number | null;
        LO: number | null;
        LA: number | null;
        weight: number | null;
        habitat_name: string | null;
        age_group_name: string | null;
    }

}
