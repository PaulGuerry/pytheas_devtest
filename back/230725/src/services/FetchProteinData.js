import axios from "axios"

export class ProteinService { 

    static getEBIdata(accessionCode) {
        let dataURL = `https://www.ebi.ac.uk/proteins/api/proteins?accession=`+ accessionCode 
        return axios.get(dataURL)
    }
}