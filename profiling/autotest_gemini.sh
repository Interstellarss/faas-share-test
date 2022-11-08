# kubectl edit daemonset -n kube-system kubeshare-node-daemon
# yukiozhu/kubeshare-gemini-hook-init:debug
# yukiozhu/kubeshare-gemini-scheduler:debug2

#j gemini-hook
#docker build --no-cache -f docker/kubeshare-gemini-hook-init/Dockerfile -t yukiozhu/kubeshare-gemini-hook-init:debug .
#docker push yukiozhu/kubeshare-gemini-hook-init:debug

kubectl delete pod -n kube-system -l lsalab=kubeshare-node-daemon
#sleep 15
kubectl delete sharepod -n faas-share-fn shufflenet
kubectl delete pod -n faas-share-fn -l app=shufflenet --force
sleep 10
kubectl create -f /home/ubuntu/go/src/github.com/Interstellarss/faas-share/Action/shufflenet.yaml
