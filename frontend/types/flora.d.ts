export {}

declare global {
    interface FloraRescueData {
        epiphyte_number: number;
        rescue_date: Date;
        rescue_area_latitude: number;
        rescue_area_longitude: number;
        substrate: string;
        dap_bryophyte: number;
        height_bryophyte: number;
        bryophyte_position: number;
        growth_habit: string;
        epiphyte_phenology: string;
        health_status_epiphyte: string;
        microhabitat: string;
        other_observations: string;
        specie_bryophyte_id: number;
        genus_bryophyte_id: number;
        family_bryophyte_id: number;
        specie_epiphyte_id: number;
        genus_epiphyte_id: number; 
        family_epiphyte_id: number;
        rescue_zone_id: number;
        id: number;
    }

    interface FloraRescueSpeciesData{
        epiphyte_number: string; 
        rescue_date: Date; 
        rescue_area_latitude: number;
        rescue_area_longitude: number; 
        specie_name: string | None;
        genus_name: string | None;
        family_name: string| None;
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
