export {}

declare global {
    interface TransectHerpetoTransWithSpeciesData{
        cod: string; 
        date: Date;
        latitude_in: number;
        longitude_in: number;
        altitude_in: number;
        latitude_out: number;
        longitude_out: number;
        altitude_out: number;
        specie_names: string[];
        total_translocation: number;
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
    interface PointHerpetoTransloWithSpeciesData{
        cod: string;
        date: Date;
        latitude: number; 
        longitude: number; 
        altitude: number; 
        specie_names: string[];
        total_translocation: number; 
    }
}
