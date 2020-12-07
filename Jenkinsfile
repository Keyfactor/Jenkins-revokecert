pipeline {
    agent any
    parameters {
        string(name: 'StoreID', defaultValue: '100000')
        string(name: 'Reason', defaultValue: '0', description: '0: Unspecified\n1: Key Compromised\n3: CA Compromised')
        string(name: 'Comment', defaultValue: 'Revocation comment')
    }
    stages {
        stage('Revoke certificate in Keyfactor') {
            steps {
                echo "Calling KeyFactor"
                withEnv(['PATH+EXTRA=/usr/sbin:/usr/bin:/sbin:/bin']) {
                    sh "python3 main.py ${params.StoreID} ${params.Reason} \"${params.Comment}\""
                }
            }
        }
    }
}