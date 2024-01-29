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
    interface FloraRelocationWithSpecieData{
        relocation_date: Date;
        flora_rescue: string;
        specie_name_epiphyte: string | null; 
        genus_name_epiphyte: string | null;
        family_name_epiphyte: string | null;
        size: number;
        epiphyte_phenology: string;
        johanson_zone: string | null;
        relocation_position_latitude: number;
        relocation_position_longitude: number;
        relocation_position_altitude: number; 
        dap_bryophyte: number | null;
        height_bryophyte: number | null;
        bark_type:  string | null;
        infested_lianas: string | null;
        other_observations:  string | null;
        specie_name_bryophyte: string | null;
        genus_name_bryophyte: string | null;
        family_name_bryophyte: string | null;
        relocation_zone: string;
    }

}

