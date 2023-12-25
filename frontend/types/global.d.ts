export {}

declare global {
        interface TransectHerpetofaunaData {
                number:string;
                date_in:Date;
                date_out:Date;
                latitude_in:number;
                longitude_in:number;
                altitude_in:number;
                latitude_out:number;
                longitude_out:number;
                altitude_out:number;
                tower_id:number;
        }

        interface TransectHerpetoWithSpecies{
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

        interface RescueMammalsWithSpecieData{
                cod: string; 
                date: Date; 
                longitude: number; 
                latitude: number; 
                observation: string|null;
                specie_name: string | null; 
                genus_name: string | null;
        }

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
        
        interface FloraRescueSpeciesData{
                epiphyte_number: string; 
                rescue_date: Date; 
                rescue_area_latitude: number;
                rescue_area_longitude: number; 
                specie_name: string | None;
                genus_name: string | None;
                family_name: string| None;
        }

        interface ImageSpecieData {
                url: string;
                atribute: string;
                specie_id: number;
        }
        interface SpecieItemData{
                id: number;
                scientific_name: string;
                specie_name: string;
                genus_full_name: string;
                family_name: string;
                order_name: string;
                class_name: string;
                images: ImageSpecieData[];
                total_rescues:number;
        }
        interface Token {
                token: string;
        }
}


