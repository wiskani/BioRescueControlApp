export {};

declare global {
    interface FloraRescueSpeciesData {
        epiphyte_number: string; 
        rescue_date: Date;
        rescue_area_latitude: number;
        rescue_area_longitude: number; 
        specie_name: string | null; 
        genus_name: string | null; 
        family_name: string| null; 
    }

    interface TransectHerpetoWithSpeciesData {
        number: string; 
        date_in: Date; 
        date_out: Date; 
        latitude_in: number; 
        longitude_in: number; 
        latitude_out: number; 
        longitude_out: number; 
        specie_names: string[]; 
        total_rescue: number; 
    }

    interface RescueMammalsWithSpecieData {
        cod: string; 
        date: Date; 
        longitude: number; 
        latitude: number ;
        observation: string|null; 
        specie_name: string | null; 
        genus_name: string | null; 
    }

}

