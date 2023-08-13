export {}

declare global {
    interface FloraRescueData {
        epiphyte_number: number;
        rescue_date: string;
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
        rescue_zone_id: number;
        id: number;
    }
    interface Token {
        token: string;
    }
}


