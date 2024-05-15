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
}
