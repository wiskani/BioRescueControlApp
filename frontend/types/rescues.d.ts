export {};

declare global {
    interface FloraRescueSpeciesData{
        epiphyte_number: string; 
        rescue_date: Date; 
        rescue_area_latitude: number;
        rescue_area_longitude: number; 
        specie_name: string | None;
        genus_name: string | None;
        family_name: string| None;
        family_name: string | None
        substrate: string | None
        dap_bryophyte: number | None
        height_bryophyte: number | None
        bryophyte_position: number | None
        growth_habit: string | None
        epiphyte_phenology: string | None
        health_status_epiphyte: string | None
        microhabitat: string | None
        other_observations: string | None
        is_epiphyte_confirmed: boolean
        is_bryophyte_confirmed: boolean
        specie_bryophyte_name: string | None
        genus_bryophyte_name: string | None
        family_bryophyte_name: string | None
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

