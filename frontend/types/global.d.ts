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
                status_name: string;
                images: ImageSpecieData[];
                total_rescues:number;
        }
        interface Token {
                token: string;
        }
}


